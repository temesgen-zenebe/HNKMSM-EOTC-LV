from django.urls import path
from .views import stripe_webhook
from .views import (
    AddToPaymentCaseCartView, 
    CheckoutView, 
    PaymentCaseCartListView, 
    PaymentCaseListView, 
    PaymentCaseDetailView, 
    PaymentConfirmationView, 
    stripe_webhook 
)

app_name = 'payments' 

urlpatterns = [
    path('payment-cases/', PaymentCaseListView.as_view(), name='payment_case_list'),
    path('payment-cases/<slug:slug>/', PaymentCaseDetailView.as_view(), name='payment_case_detail'),
    path('addToPaymentCaseCartView/<slug:slug>/', AddToPaymentCaseCartView.as_view(), name='addToPaymentCaseCart_view'),
    path('paymentCaseCartView/', PaymentCaseCartListView.as_view(), name='paymentCaseCart_view'),
    path('checkout/', CheckoutView.as_view(), name='checkout_view'),
    path('confirmation/', PaymentConfirmationView.as_view(), name='payment_confirmation'),
    path('webhook/', stripe_webhook, name='stripe-webhook'),

    # Add other URL patterns as needed
]
