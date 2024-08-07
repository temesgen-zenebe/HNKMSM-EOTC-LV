from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView,ListView,DetailView
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from .models import PaymentCase, PaymentCaseCartList,BillingInformation, Payment,PaymentHistory, PaymentCaseLists
from members.models import MembersUpdateInformation
from django.views.generic import FormView
from .forms import BillingForm, CardInformationForm
import uuid
import json
import stripe
import logging
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json



class PaymentCaseListView(ListView):
    model = PaymentCaseLists
    template_name = 'payments/payment_case_list.html'  # Specify your template name
    context_object_name = 'payment_cases'  # Specify the context object name to use in the template
    paginate_by = 10  # Optional: to paginate the list if there are many items

class PaymentCaseDetailView(DetailView): 
    model = PaymentCaseLists
    template_name = 'payments/payment_case_detail.html'  # Specify your detail view template
    context_object_name = 'payment_case'

class AddToPaymentCaseCartView(View):
    
    def post(self, request, slug):
        payment_case = get_object_or_404(PaymentCase, slug=slug)
        cart_item, created = PaymentCaseCartList.objects.get_or_create(user=request.user, payment_case=payment_case)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect('payments:paymentCaseCart_view')
    
class PaymentCaseCartListView(LoginRequiredMixin,ListView):
    model = PaymentCaseCartList
    template_name = 'payments/paymentCaseCart_list.html'
    context_object_name = 'paymentCaseCart_items'

    def get_queryset(self):
        return PaymentCaseCartList.objects.filter(user=self.request.user)
    
class CheckoutView(FormView):
    template_name = 'payments/checkout.html'
    form_class = BillingForm
    success_url = reverse_lazy('payments:payment_confirmation') # Redirect to a confirmation page after successful payment

    def get_form_kwargs(self):
        kwargs = super(CheckoutView, self).get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the user to the form
        return kwargs
    
    
    def form_valid(self, form):
        # Save billing information
        billing_info = form.save(commit=False)
        billing_info.user = self.request.user
        billing_info.save()
        
        # Use the payment_case value from the form
        payment_case_value = form.cleaned_data.get('payment_case')   
        # Process the payment using Stripe
        # This is where you would use Stripe's API to create a charge
        # Mocking Stripe payment for simplicity
        payment = Payment(
            user=self.request.user,
            billing_info=billing_info,
            payment_case = payment_case_value,
            amount=100.00,  # Replace with the actual amount from your cart
            payment_id=str(uuid.uuid4()),  # Use actual Stripe payment ID
            status='Success'
        )
        payment.save()
        
       
        

        if payment_case_value == 'membership':
            try:
                membership = MembersUpdateInformation.objects.get(user=self.request.user)
                membership.member_status = 'active'
                membership.save()

            except MembersUpdateInformation.DoesNotExist:
                # Handle the case where the user does not have a membership info record
                pass
        
        # Clear the cart
        PaymentCaseCartList.objects.filter(user=self.request.user).delete()
        
        return super().form_valid(form)

class PaymentConfirmationView(TemplateView):
    template_name = 'payments/payment_confirmation.html'
    
# Set your secret key. Remember to switch to your live secret key in production.
# This is your Stripe CLI webhook secret for testing your endpoint locally.
stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

logger = logging.getLogger(__name__)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    # Log the received payload
    logger.info(f"Received payload: {payload}")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
        logger.info("Signature verification succeeded.")
    except ValueError as e:
        logger.error(f"Invalid payload: {e}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Invalid signature: {e}")
        return HttpResponse(status=400)

    logger.info(f"Received event type: {event['type']}")

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        logger.info(f"Checkout session completed: {json.dumps(session, indent=2)}")
        handle_checkout_session(session)

    return HttpResponse(status=200)

def handle_checkout_session(session):
    try:
        
        print(session)
        # Retrieve the user or customer email from the session
        customer_email = session.get('customer_details', {}).get('email')
        print(customer_email)
        # Retrieve the membershipID from the session's custom_fields
        custom_fields = session.get('custom_fields', [])
        # Initialize membershipID as None in case it is not found
        membershipID = None
        # Iterate over the custom_fields to find the one with key 'membershipid'
        for field in custom_fields:
            if field.get('key') == 'membershipid':
              membershipID = field.get('text', {}).get('value')
              break  # Exit loop once the membershipID is found
        # Now, membershipID will contain the value or None if not found
        print("membershipID : " + membershipID)
        
           # Retrieve and process amount and created timestamp
        amount = session['amount_total'] / 100  # Amount in dollars
        print(f"Amount: ${amount:.2f}")

        created_timestamp = session['created']
        created_date = datetime.fromtimestamp(created_timestamp).strftime('%Y-%m-%d %H:%M:%S')
        print(f"Created: {created_date}")
        
        payment_intent_id = session.get('payment_intent')
        payment_case_link = session.get('payment_link')  # Adjust this based on actual session structure
        
        print(payment_case_link)
        if not payment_case_link:
            logger.error(f"No valid payment link found in session object: {json.dumps(session, indent=2)}")
            return

        payment_case = PaymentCaseLists.objects.get(payment_case_link=payment_case_link)
        print(payment_case)
        
        # Assuming the use of Django ORM and MembersUpdateInformation model
        user = None
        if membershipID:
            try:
                #Retrieve the first member that matches the membershipID
                member = MembersUpdateInformation.objects.filter(member_id=membershipID).first()
        
                # Check if a member was found and get the user associated with the member
                if member:
                   user = member.user
                   if payment_case == 'membership':
                      member.member_status = 'active'
                      member.save()
                   
                   # Print the user information
                   print(f"user: {user}")
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            print("No membershipID found.")
        
        
        PaymentHistory.objects.create(
            user = user,
            payment_email=customer_email,
            #paymentConfirmation=payment_intent_id,
            amount=amount,
            payment_case=payment_case,
            payment_date=created_date
           
        )
        logger.info("PaymentHistory record created successfully.")
    except PaymentCaseLists.DoesNotExist:
        logger.error(f"No PaymentCaseLists found with stripsPayment_link: {payment_case_link}")
    except Exception as e:
        logger.error(f"Error handling checkout session: {e}")


 
