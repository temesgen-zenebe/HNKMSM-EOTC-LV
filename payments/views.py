from pyexpat.errors import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from django.views.generic import TemplateView,ListView,DetailView
from django.views.generic.edit import DeleteView, UpdateView
from django.views import View
from django.shortcuts import get_object_or_404, redirect, render
from members.models import MembersUpdateInformation
from django.views.generic import FormView
import uuid
import json
import stripe
import logging
from datetime import datetime
from django.utils import timezone
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import PaymentCaseCartForm  # Assume you have created a form for updating
from decimal import Decimal
from .models import (
    PaymentCases,
    CartPayment,
    CartPaymentCases,
    Category,
    Order, 
    ShippingInformation, 
    OrderCase,
    )

class PaymentMenuView(ListView):
    model = PaymentCases
    template_name = 'payments/paymentMenu.html'
    context_object_name = 'paymentLink'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payment_cases'] = PaymentCases.objects.filter(slug='membership')
        return context

class PaymentCaseListView(ListView):
    model = PaymentCases
    template_name = 'payments/payment_case_list.html'  # Specify your template name
    context_object_name = 'payment_cases'  # Specify the context object name to use in the template
    paginate_by = 10  # Optional: to paginate the list if there are many items
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        payment_cases = PaymentCases.objects.all()

        context.update({
            'payment_service_cases': payment_cases.filter(category__title='service'),
            'payment_donation_cases': payment_cases.filter(category__title='donation'),
            'payment_other_cases': payment_cases.exclude(category__title='service'),
            'payment_products_cases': payment_cases.filter(category__title='product'),
        })

        return context

class PaymentCaseDetailView(DetailView): 
    model = PaymentCases
    template_name = 'payments/payment_case_detail.html'  # Specify your detail view template
    context_object_name = 'payment_case'
     
class AddToPaymentCaseCartView(LoginRequiredMixin, View):
    def post(self, request, slug):
        # Fetch the PaymentCase instance by slug
        payment_case = get_object_or_404(PaymentCases, slug=slug)
        
        # Get the user's membership information
        membership = MembersUpdateInformation.objects.filter(user=request.user).first()
        
        # Ensure the user has only one active cart; create if none exists
        cart, _ = CartPayment.objects.get_or_create(
            user=request.user,
            membersID=membership  # Ensure this is the correct membership instance
        )
        
        # Check if the item already exists in the cart
        cart_item, created = CartPaymentCases.objects.get_or_create(
            cart=cart,
            user=request.user,
            payment_case=payment_case,  # Link the PaymentCase instance
            defaults={'quantity': 1}  # Set default quantity for new cart item
        )
        
        # If the cart item already exists, increment the quantity
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        # Redirect to the cart view after processing
        return redirect('payments:paymentCaseCart_view')

class PaymentCaseCartListView(LoginRequiredMixin, ListView):
    model = CartPaymentCases  # Use the correct model
    template_name = 'payments/checkout.html'  # Specify your template
    context_object_name = 'payment_cases_cart'  # The name used in the template

    def get_queryset(self):
        """
        Override get_queryset to filter cart items by the logged-in user.
        """
        return CartPaymentCases.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        """
        Add additional context to the template.
        """
        context = super().get_context_data(**kwargs)
        
        # Fetch the filtered queryset (cart items for the logged-in user)
        payment_cases_cart = self.get_queryset()

        # Membership information (assuming one-to-one relation with user)
        membership = MembersUpdateInformation.objects.filter(user=self.request.user).first()

        # Determine if any item requires delivery
        requires_delivery = payment_cases_cart.filter(payment_case__requires_delivery=True).exists()
        
        # Calculate totals and enrich context
        for case in payment_cases_cart:
            case.total_price = case.quantity * case.payment_case.amount

        total = sum(case.total_price for case in payment_cases_cart)
        cart_count = sum(case.quantity for case in payment_cases_cart)
        shipping_cost = sum(case.payment_case.shipping_cost for case in payment_cases_cart)
        # Add data to the context
        context.update({
            'payment_cases_cart': payment_cases_cart,  # List of items in the cart
            'checkout_total': total + shipping_cost ,              # Total price of all items
            'cart_count': cart_count,                 # Number of items in the cart
            'membership': membership,                 # Membership information
            'requires_delivery': requires_delivery,   # Delivery requirement flag
            'shipping_cost':shipping_cost,
        })
        return context

class PaymentCaseCartDeleteView(LoginRequiredMixin,DeleteView):
    model = CartPaymentCases
    template_name = 'payments/delete_case_cart.html'  # Template for confirmation (optional)
    success_url = reverse_lazy('payments:paymentCaseCart_view')  # Redirect to the cart list view after deletion

    def get_queryset(self):
        # Optional: Filter queryset if needed, e.g., by user
        return super().get_queryset()

class PaymentCaseCartUpdateView(LoginRequiredMixin, UpdateView):
    model = CartPaymentCases
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
   
class PaymentCancelView(TemplateView):
    template_name = "payments/cancel.html"
    
class PaymentSuccessView(TemplateView):
    template_name = "payments/success.html"
   
    
# Set your secret key. Remember to switch to your live secret key in production.
# This is your Stripe CLI webhook secret for testing your endpoint locally.
stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
logger = logging.getLogger(__name__)


class CheckoutActionView(View):
    def post(self, request, *args, **kwargs):
        # Retrieve cart items and calculate total price
        cart_items = CartPaymentCases.objects.filter(user=request.user)
        if not cart_items.exists():
            return JsonResponse({'error': 'Cart is empty'}, status=400)

        total_amount = sum(item.payment_case.amount * item.quantity for item in cart_items)
        
        # Determine if any items require delivery
        requires_delivery = any(item.payment_case.requires_delivery for item in cart_items)
        
        #calculating total_delivery
        if requires_delivery :
           total_delivery = 10 #sum(item.payment_case.shipping_cost for item in cart_items)
        else : total_delivery=0
        
        # Prepare shipping details conditionally
        shipping_address_collection = {
            "allowed_countries": ["US", "CA", "GB", "DE", "AU", "FR", "IN", "ET"]
        } if requires_delivery else {}

        shipping_options = [
            {
                "shipping_rate_data": {
                    "type": "fixed_amount",
                    "fixed_amount": {"amount": total_delivery, "currency": "usd"},
                    "display_name": "Standard Shipping",
                    "delivery_estimate": {
                        "minimum": {"unit": "business_day", "value": 3},
                        "maximum": {"unit": "business_day", "value": 7},
                    },
                    "metadata": {
                        "shipping_type": "Standard",
                        "estimated_delivery": "3-7 business days",
                    },
                },
            },
        ] if requires_delivery else []

        # Create a new order
        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            payment_status="pending"
        )

        # Create a Stripe checkout session
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {"name": item.payment_case.title},
                            "unit_amount": int(item.payment_case.amount * 100),  # Convert to cents
                        },
                        "quantity": item.quantity,
                    }
                    for item in cart_items
                ],
                mode="payment",
                success_url=request.build_absolute_uri(reverse("payments:success")),
                cancel_url=request.build_absolute_uri(reverse("payments:cancel")),
                shipping_address_collection=shipping_address_collection,
                shipping_options=shipping_options,
                metadata={
                    "order_id": str(order.order_id),
                    # "membersID": cart_items.cart.membersID
                },  # Pass order ID for webhook
            )

            return JsonResponse({"checkout_url": session.url})

        except stripe.error.StripeError as e:
            return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET  # Add your Stripe webhook secret in settings

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        return JsonResponse({"error": "Invalid payload"}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({"error": "Invalid signature"}, status=400)

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        # Retrieve order_id from session metadata
        order_id = session["metadata"]["order_id"]

        # Update order status to "completed"
        order = Order.objects.filter(order_id=order_id).first()
        if order:
            order.payment_status = "completed"
            order.save()

            # Update OrderCase information
            order_cases = OrderCase.objects.filter(order=order)
            for order_case in order_cases:
                if order_case.payment_case.requires_delivery:
                    order_case.delivery_state = "pending"  # Mark as pending for delivery
                else:
                    order_case.delivery_state = "delivered"  # No delivery required
                order_case.save()

            # Update or create ShippingInformation
            if session.get("shipping"):
                shipping_details = session["shipping"]["address"]
                shipping_info, created = ShippingInformation.objects.update_or_create(
                    user=order.user,
                    defaults={
                        "address": shipping_details.get("line1"),
                        "address2": shipping_details.get("line2"),
                        "country": shipping_details.get("country"),
                        "state": shipping_details.get("state"),
                        "zip_code": shipping_details.get("postal_code"),
                    },
                )

    return JsonResponse({"status": "success"})


# @csrf_exempt
# def stripe_webhook(request):
#     payload = request.body
#     sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
#     event = None

#     # Log the received payload
#     logger.info(f"Received payload: {payload}")
    
#     if sig_header is None:
#         logger.error("Missing Stripe-Signature header")
#         return JsonResponse({'error': 'Missing Stripe-Signature header'}, status=400)

#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
#         )
#         logger.info("Signature verification succeeded.")
#     except ValueError as e:
#         logger.error(f"Invalid payload: {e}")
#         return HttpResponse(status=400)
#     except stripe.error.SignatureVerificationError as e:
#         logger.error(f"Invalid signature: {e}")
#         return HttpResponse(status=400)

#     logger.info(f"Received event type: {event['type']}")

#     if event['type'] == 'checkout.session.completed':
#         session = event['data']['object']
#         logger.info(f"Checkout session completed: {json.dumps(session, indent=2)}")
#         handle_checkout_session(session)

#     return HttpResponse(status=200)

# def handle_checkout_session(session):
#     try:
        
#         print(session)
#         # Retrieve the user or customer email from the session
#         customer_email = session.get('customer_details', {}).get('email')
#         print(customer_email)
#         # Retrieve the membershipID from the session's custom_fields
#         custom_fields = session.get('custom_fields', [])
#         # Initialize membershipID as None in case it is not found
#         membershipID = None
#         # Iterate over the custom_fields to find the one with key 'membershipid'
#         for field in custom_fields:
#             if field.get('key') == 'membershipid':
#               membershipID = field.get('text', {}).get('value')
#               break  # Exit loop once the membershipID is found
#         # Now, membershipID will contain the value or None if not found
#         print("membershipID : " + membershipID)
        
#            # Retrieve and process amount and created timestamp
#         amount = session['amount_total'] / 100  # Amount in dollars
#         print(f"Amount: ${amount:.2f}")

#         created_timestamp = session['created']
#         created_date = datetime.fromtimestamp(created_timestamp).strftime('%Y-%m-%d %H:%M:%S')
#         print(f"Created: {created_date}")
        
#         payment_intent_id = session.get('payment_intent')
#         payment_case_link = session.get('payment_link')  # Adjust this based on actual session structure
        
#         print(payment_case_link)
#         if not payment_case_link:
#             logger.error(f"No valid payment link found in session object: {json.dumps(session, indent=2)}")
#             return

#         payment_case = PaymentCaseLists.objects.get(payment_case_link=payment_case_link)
#         print(payment_case)
        
#         # # Create a Stripe Checkout session
#         # checkout_session = stripe.checkout.Session.create(
#         #     mode="payment",
#         #     invoice_creation={"enabled": True},
#         #     line_items=[{"price": "price_1PXL9PP9YIWmSYJtvyb5XX4k", "quantity": 1}],  # Replace with your actual price ID
#         #     success_url="http://127.0.0.1:8000/payments/confirmation/",
#         #     #cancel_url="https://yourwebsite.com/cancel",
#         #     customer_email=customer_email  # Automatically fill the email in the Stripe checkout
#         # )
        
        
#         # Assuming the use of Django ORM and MembersUpdateInformation model
#         user = None
#         if membershipID:
#             #print(f"Searching for member with membershipID: {membershipID}")
#             try:
#                 #Retrieve the first member that matches the membershipID
#                 member = MembersUpdateInformation.objects.filter(member_id=membershipID).first()
        
#                 # Check if a member was found and get the user associated with the member
#                 if member:
#                     #print(f"Member found: {member.full_name}")
#                     user = member.user
#                     if payment_case.title == 'membership':
#                         #print(f"Updating member status to active for member: {member.full_name}")
#                         member.member_status = 'active'
#                         member.save()
#                    # Print the user information
#                     print(f"user: {user}")
                   
#                 if member.member_status == 'pending':
#                     print(f"member_status change to: {member.member_status}")
                    
#             except Exception as e:
#                 print(f"An error occurred: {e}")
#         else:
#             print("No membershipID found.")
        
#         # PaymentHistory.objects.create(
#         #     user = user,
#         #     payment_email=customer_email,
#         #     #paymentConfirmation=payment_intent_id,
#         #     amount=amount,
#         #     payment_case=payment_case,
#         #     payment_date=timezone.now() #created_date 
           
#         # )
        
#         logger.info("PaymentHistory record created successfully.")
        
#         # Redirect the user to the Stripe-hosted payment_confirmation page
#         return redirect('http://127.0.0.1:8000/payments/confirmation/')

#     except PaymentCaseLists.DoesNotExist:
#         logger.error(f"No PaymentCaseLists found with stripsPayment_link: {payment_case_link}")
#     except Exception as e:
#         logger.error(f"Error handling checkout session: {e}")





