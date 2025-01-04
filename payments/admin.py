
from django.contrib import admin
from .models import (
    PaymentCases,
    CartPayment,
    CartPaymentCases,
    Category,
    
)
admin.site.register(PaymentCases)
admin.site.register(CartPayment)
admin.site.register(CartPaymentCases)
admin.site.register(Category)



