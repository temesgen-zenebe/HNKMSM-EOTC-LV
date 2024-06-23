from django.urls import path
from .views import PaymentCaseListView, PaymentCaseDetailView, add_to_cart  # Import your views

app_name = 'payments' 

urlpatterns = [
    path('payment-cases/', PaymentCaseListView.as_view(), name='payment_case_list'),
    path('payment-cases/<slug:slug>/', PaymentCaseDetailView.as_view(), name='payment_case_detail'),
    path('payment-cases/add-to-cart/<slug:slug>/', add_to_cart, name='add_to_cart'),
    # Add other URL patterns as needed
]
