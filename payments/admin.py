from django.contrib import admin
from .models import (
    BillingInformation, 
    Categories, Payment, 
    PaymentCase, 
    PaymentCaseCartList,
    PaymentHistory,
    PaymentCaseLists,
    )

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
admin.site.register(PaymentCaseLists)
# admin.site.register(PaymentHistory)

# Customizing the admin interface for PaymentHistory
from django.contrib import admin
from django.db.models import Sum  # Import Sum from django.db.models
from .models import PaymentHistory

# Customizing the admin interface for PaymentHistory
class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_email', 'amount', 'payment_case', 
                    'payment_date', 'created', 'slug', 'cumulative_total')
    list_filter = ('payment_date', 'created', 'payment_case')
    search_fields = ('user__username', 'payment_email', 'paymentConfirmation')
    readonly_fields = ('paymentConfirmation', 'created', 'payment_date')  # Add 'payment_date' here
    ordering = ('-created',)  # Order by creation date descending
    #prepopulated_fields = {'slug': ('payment_case',)}

    # Optionally, you can customize the admin form
    fieldsets = (
        (None, {
            'fields': ('user', 'payment_email', 'amount', 'payment_case')
        }),
        ('Date Information', {
            'fields': ('created',),
            'classes': ('collapse',),
        }),
    )

    def cumulative_total(self, obj):
        # Calculate the cumulative total of payments for the user
        total = PaymentHistory.objects.filter(user=obj.user).aggregate(total_amount=Sum('amount'))['total_amount']
        return f"${total:.2f}" if total is not None else "$0.00"

    cumulative_total.short_description = 'Cumulative Total'  # Customize the column header

# Register the model with the custom admin class
admin.site.register(PaymentHistory, PaymentHistoryAdmin)

