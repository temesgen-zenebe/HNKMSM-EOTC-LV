from django.contrib import admin
from .models import Categories, PaymentCase

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
