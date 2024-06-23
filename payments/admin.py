from django.contrib import admin
from .models import BillingInformation, Categories, Payment, PaymentCase, PaymentCaseCartList

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "created", "updated")
    search_fields = ("title", "description")

@admin.register(PaymentCase)
class PaymentCaseAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "category", "amount", "created", "updated")
    search_fields = ("title", "description", "category__title")
    list_filter = ("category", "created", "updated")
    
admin.site.register(BillingInformation)
admin.site.register(PaymentCaseCartList)
admin.site.register(Payment)