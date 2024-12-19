
from django.contrib import admin
from .models import (
    PaymentCaseLists,
    OrderPaymentCase,
    CartPaymentCase
)
admin.site.register(PaymentCaseLists)
admin.site.register(OrderPaymentCase)
admin.site.register(CartPaymentCase)

