from pyexpat.errors import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView,ListView,DetailView
from django.views.generic.edit import DeleteView, UpdateView
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from members.models import MembersUpdateInformation
from django.views.generic import FormView
import uuid
from django.http import JsonResponse
import json
import stripe
import logging
from datetime import datetime
from django.utils import timezone
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import PaymentCaseLists, CartPaymentCase
from .forms import PaymentCaseCartForm  # Assume you have created a form for updating

class PaymentMenuView(ListView):
    model = PaymentCaseLists
    template_name = 'payments/paymentMenu.html'
    context_object_name = 'paymentLink'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payment_cases'] = PaymentCaseLists.objects.filter(slug='membership')
        return context

class PaymentCaseListView(ListView):
    model = PaymentCaseLists
    template_name = 'payments/payment_case_list.html'  # Specify your template name
    context_object_name = 'payment_cases'  # Specify the context object name to use in the template
    paginate_by = 10  # Optional: to paginate the list if there are many items
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payment_service_cases'] = PaymentCaseLists.objects.filter(category='service')
        context['payment_Other_cases'] = PaymentCaseLists.objects.exclude(category='service')
        context['payment_donation_cases'] = PaymentCaseLists.objects.filter(category='donation')
        return context

class PaymentCaseDetailView(DetailView): 
    model = PaymentCaseLists
    template_name = 'payments/payment_case_detail.html'  # Specify your detail view template
    context_object_name = 'payment_case'
     
class AddToPaymentCaseCartView(LoginRequiredMixin ,View):
    
    def post(self, request, slug):
        payment_case = get_object_or_404(PaymentCaseLists, slug=slug)
        membership = MembersUpdateInformation.objects.filter(user=request.user).first()
        
        cart_item, created = CartPaymentCase.objects.get_or_create(
            user=request.user,
            membersID=membership,  # Ensure this is the correct instance
            payment_cases=payment_case,  # Pass the correct ForeignKey instance
            defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect('payments:paymentCaseCart_view')


class PaymentCaseCartListView(LoginRequiredMixin, ListView):
    model = CartPaymentCase  # Use the correct model
    template_name = 'payments/checkout.html'  # Specify your template
    context_object_name = 'payment_cases_cart'  # The name used in the template

    def get_queryset(self):
        """
        Override get_queryset to filter cart items by the logged-in user.
        """
        return CartPaymentCase.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        """
        Add additional context to the template.
        """
        context = super().get_context_data(**kwargs)
        
        # Fetch the filtered queryset (cart items for the logged-in user)
        payment_cases_cart = self.get_queryset()

        # Membership information (assuming one-to-one relation with user)
        membership = MembersUpdateInformation.objects.filter(user=self.request.user).first()

        # Calculate totals and enrich context
        for case in payment_cases_cart:
            case.total = case.quantity * case.payment_cases.amount

        total = sum(case.total for case in payment_cases_cart)
        cart_count = payment_cases_cart.count()

        # Add data to the context
        context.update({
            'payment_cases_cart': payment_cases_cart,
            'checkout_total': total,
            'cart_count': cart_count,
            'membership': membership,
        })

        return context

class PaymentCaseCartDeleteView(LoginRequiredMixin,DeleteView):
    model = CartPaymentCase
    template_name = 'payments/delete_case_cart.html'  # Template for confirmation (optional)
    success_url = reverse_lazy('payments:paymentCaseCart_view')  # Redirect to the cart list view after deletion

    def get_queryset(self):
        # Optional: Filter queryset if needed, e.g., by user
        return super().get_queryset()

class PaymentCaseCartUpdateView(LoginRequiredMixin, UpdateView):
    model = CartPaymentCase
    form_class = PaymentCaseCartForm  # Form for updating the cart case
    template_name = 'payments/update_case_cart.html'  # Template for updating
    success_url = reverse_lazy('payments:paymentCaseCart_view')  # Redirect to the cart list view after update

    def get_queryset(self):
        # Optional: Filter queryset if needed, e.g., by user
        return super().get_queryset()

# class PaymentsHistoryListView(LoginRequiredMixin,ListView):
#     model = PaymentHistory
#     template_name = 'payments/paymentHistory_list.html'
#     context_object_name = 'paymentHistoryList'
#     #success_url = reverse_lazy('payments:payment_confirmation')

#     def get_queryset(self):
#         return PaymentHistory.objects.filter(user=self.request.user)
    


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
    
    if sig_header is None:
        logger.error("Missing Stripe-Signature header")
        return JsonResponse({'error': 'Missing Stripe-Signature header'}, status=400)

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
        
        # # Create a Stripe Checkout session
        # checkout_session = stripe.checkout.Session.create(
        #     mode="payment",
        #     invoice_creation={"enabled": True},
        #     line_items=[{"price": "price_1PXL9PP9YIWmSYJtvyb5XX4k", "quantity": 1}],  # Replace with your actual price ID
        #     success_url="http://127.0.0.1:8000/payments/confirmation/",
        #     #cancel_url="https://yourwebsite.com/cancel",
        #     customer_email=customer_email  # Automatically fill the email in the Stripe checkout
        # )
        
        
        # Assuming the use of Django ORM and MembersUpdateInformation model
        user = None
        if membershipID:
            #print(f"Searching for member with membershipID: {membershipID}")
            try:
                #Retrieve the first member that matches the membershipID
                member = MembersUpdateInformation.objects.filter(member_id=membershipID).first()
        
                # Check if a member was found and get the user associated with the member
                if member:
                    #print(f"Member found: {member.full_name}")
                    user = member.user
                    if payment_case.title == 'membership':
                        #print(f"Updating member status to active for member: {member.full_name}")
                        member.member_status = 'active'
                        member.save()
                   # Print the user information
                    print(f"user: {user}")
                   
                if member.member_status == 'pending':
                    print(f"member_status change to: {member.member_status}")
                    
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            print("No membershipID found.")
        
        # PaymentHistory.objects.create(
        #     user = user,
        #     payment_email=customer_email,
        #     #paymentConfirmation=payment_intent_id,
        #     amount=amount,
        #     payment_case=payment_case,
        #     payment_date=timezone.now() #created_date 
           
        # )
        
        logger.info("PaymentHistory record created successfully.")
        
        # Redirect the user to the Stripe-hosted payment_confirmation page
        return redirect('http://127.0.0.1:8000/payments/confirmation/')

    except PaymentCaseLists.DoesNotExist:
        logger.error(f"No PaymentCaseLists found with stripsPayment_link: {payment_case_link}")
    except Exception as e:
        logger.error(f"Error handling checkout session: {e}")


 
