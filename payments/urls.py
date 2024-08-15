from django.urls import path
#from .views import stripe_webhook
from . import views  # Import your view handling the webhook
from .views import (
    AddToPaymentCaseCartView, 
    CheckoutView, 
    PaymentsHistoryListView, 
    PaymentCaseListView, 
    PaymentCaseDetailView, 
    PaymentConfirmationView, 
    PaymentMenuView,
    #stripe_webhook 
)

app_name = 'payments' 

urlpatterns = [
    path('payment-menu/', PaymentMenuView.as_view(), name='payment_menu'),
    path('payment-cases/', PaymentCaseListView.as_view(), name='payment_case_list'),
    path('payment-cases/<slug:slug>/', PaymentCaseDetailView.as_view(), name='payment_case_detail'),
    path('addToPaymentCaseCartView/<slug:slug>/', AddToPaymentCaseCartView.as_view(), name='addToPaymentCaseCart_view'),
    path('paymentsHistoryList/', PaymentsHistoryListView.as_view(), name='paymentsHistoryList'),
    path('checkout/', CheckoutView.as_view(), name='checkout_view'),
    path('confirmation/', PaymentConfirmationView.as_view(), name='payment_confirmation'),
    #path('webhook/', stripe_webhook, name='stripe-webhook'),
    path('stripe_webhook/', views.stripe_webhook, name='stripe_webhook'),

    # Add other URL patterns as needed
]
