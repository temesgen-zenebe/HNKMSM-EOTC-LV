
from django.contrib import admin
from .models import (
    PaymentCaseLists,
    PaymentCaseCart,
    OrderPaymentCase,
    # CartPaymentCase,
    PaymentCases,
    CartPayment,
    CartPaymentCases,
    Category,
    
)
admin.site.register(PaymentCaseLists)
admin.site.register(OrderPaymentCase)
# admin.site.register(CartPaymentCase)
admin.site.register(PaymentCaseCart)
admin.site.register(PaymentCases)
admin.site.register(CartPayment)
admin.site.register(CartPaymentCases)
admin.site.register(Category)



