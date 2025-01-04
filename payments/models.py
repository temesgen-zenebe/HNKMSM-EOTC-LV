from django.db import models
from django.conf import settings
from django.forms import ValidationError
from common.utils.text import unique_slug
from django.utils import timezone
from ckeditor.fields import RichTextField # eg. description = RichTextField()
from decimal import Decimal
import uuid
from members.models import MembersUpdateInformation

class Category(models.Model):
    title = models.CharField(max_length=255)
    sub_title=models.CharField(max_length=255,blank=True, null=True)
    description=models.TextField(max_length=255,blank=True, null=True)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
            if not self.slug:
                value = str(self.title)
                self.slug = unique_slug(value, type(self))
            super(Category, self).save(*args, **kwargs)
            
    def __str__(self):
        return self.title
    
class PaymentCases(models.Model):
    TYPE_CHOICES = (
        ('onetime', 'One-Time'),
        ('recurring', 'Recurring'),
    )
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    stripe_payment_link = models.URLField(null=True, blank=True )
    payment_case_link = models.CharField(max_length=255, blank=True, null=True)
    qr_code_image = models.ImageField(upload_to='payments/qrcodes/', blank=True, null=True)
    case_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    instructions = models.TextField(default="If you need guidance on how to make a payment, please contact the office for assistance.")
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    image = models.ImageField(upload_to='payments/case_images/', blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    requires_delivery = models.BooleanField(default=False)  # Added for delivery tracking
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
            if not self.slug:
                value = str(self.title)
                self.slug = unique_slug(value, type(self))
            super(PaymentCases, self).save(*args, **kwargs)
            
    def __str__(self):
        return self.title

class CartPayment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts')
    membersID = models.ForeignKey(MembersUpdateInformation, on_delete=models.CASCADE, related_name='members_id')
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
            if not self.slug:
                value = str(self.user)
                self.slug = unique_slug(value, type(self))
            super(CartPayment, self).save(*args, **kwargs)

    def __str__(self):
        return f"Cart {self.id} for {self.user}"

class CartPaymentCases(models.Model):
    cart = models.ForeignKey(CartPayment, on_delete=models.CASCADE, related_name='cart_items')
    payment_case = models.ForeignKey(PaymentCases, on_delete=models.CASCADE, related_name='cart_cases')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart_cases')
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
                value = f"cart_case-{self.user}-{self.payment_case.title}"
                self.slug = unique_slug(value, type(self))
        # Calculate total if `payment_cases` exists
        if self.payment_case:
            self.total_price = Decimal(self.payment_case.amount) * self.quantity
            
        super(CartPaymentCases, self).save(*args, **kwargs)

    def __str__(self):
        return f"cart_items {self.quantity} x {self.payment_case.title}"
    
