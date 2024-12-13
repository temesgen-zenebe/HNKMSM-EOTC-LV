from django.urls import path
#from .views import stripe_webhook
from . import views  # Import your view handling the webhook
from .views import (
    AddToPaymentCaseCartView,
    PaymentCaseCartDeleteView, 
    PaymentCaseCartUpdateView,
    PaymentCaseCartListView,
    CheckoutView, 
    PaymentsHistoryListView, 
    PaymentCaseListView, 
    PaymentCaseDetailView, 
    PaymentConfirmationView, 
    PaymentMenuView,
)

app_name = 'payments' 

urlpatterns = [
    path('payment-menu/', PaymentMenuView.as_view(), name='payment_menu'),
    path('payment-menu/payment-cases/', PaymentCaseListView.as_view(), name='payment_case_list'),
    path('payment-cases/<slug:slug>/detail/', PaymentCaseDetailView.as_view(), name='payment_case_detail'),
    path('payment-cases/addToPaymentCaseCartView/<slug:slug>/', AddToPaymentCaseCartView.as_view(), name='addToPaymentCaseCart_view'),
    path('payment-cases/paymentCaseCartView/', PaymentCaseCartListView.as_view(), name='paymentCaseCart_view'),
    path('payment-cases/delete/<slug:slug>/', PaymentCaseCartDeleteView.as_view(), name='DeleteCaseCart'),
    path('payment-cases/update/<slug:slug>/', PaymentCaseCartUpdateView.as_view(), name='UpdatedCaseCart'),
    path('paymentsHistoryList/', PaymentsHistoryListView.as_view(), name='paymentsHistoryList'),
    path('checkout/', CheckoutView.as_view(), name='checkout_view'),
    path('confirmation/', PaymentConfirmationView.as_view(), name='payment_confirmation'),
    path('stripe_webhook/', views.stripe_webhook, name='stripe_webhook'),

    # Add other URL patterns as needed
]

