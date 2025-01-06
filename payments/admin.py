
from django.contrib import admin
from .models import (
    PaymentCases,
    CartPayment,
    CartPaymentCases,
    Category,
    ShippingInformation,
    Order,
    OrderCase,
    
)
admin.site.register(PaymentCases)
admin.site.register(CartPayment)
admin.site.register(CartPaymentCases)
admin.site.register(Category)
admin.site.register(ShippingInformation)
admin.site.register(Order)
admin.site.register(OrderCase)



