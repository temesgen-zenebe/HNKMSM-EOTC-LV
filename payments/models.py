from django.db import models
from django.conf import settings
from django.forms import ValidationError
from common.utils.text import unique_slug
from django.utils import timezone
from ckeditor.fields import RichTextField
from decimal import Decimal
import uuid
from members.models import MembersUpdateInformation

#new strip integration  
class PaymentCaseLists(models.Model):
    Category = (
        ('service', 'service'),
        ('donation', 'donation'),  
        ('marriageSchoolRegFee' ,'marriageSchoolRegFee'), 
        ('abentChildrenRegFee' ,'abentChildrenRegFee'), 
        ('abentYouthRegFee' ,'abentYouthRegFee'), 
        ('churchProjectSupportFree' ,'churchProjectSupportFree'), 
    )
    title = models.CharField(max_length=255)
    description = RichTextField()
    stripsPayment_link = models.URLField()
    payment_case_link = models.CharField(max_length=255, blank=True, null=True)
    QRCodeImage = models.ImageField(upload_to='payments/qrcodes/', blank=True, null=True)
    case_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(max_length=50, choices=[('active', 'Active'), ('inactive', 'Inactive')])
    category = models.CharField(max_length=100, choices=Category, default='service')
    Instraction = models.TextField(default="If you need guidance on how to make a payment, please contact the office for assistance.") 
    type = models.CharField(max_length=50, choices=[('onetime', 'One-Time'), ('recurring', 'Recurring')])
    image = models.ImageField(upload_to='payments/case_images/', blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    # Save method override to create slug
    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(self.title)
            self.slug = unique_slug(value, type(self))
        super(PaymentCaseLists, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
             
class CartPaymentCase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    membersID = models.ForeignKey(MembersUpdateInformation, on_delete=models.CASCADE,blank=True, null=True)
    payment_cases = models.ForeignKey(PaymentCaseLists, on_delete=models.CASCADE, blank=True,null=True)
    quantity = models.PositiveIntegerField(default=1)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)
    
    # Save method override to create slug
    def save(self, *args, **kwargs):
        if not self.slug:
            value = f"cart-{self.user.username}-{self.created}"
            self.slug = unique_slug(value, type(self)) 
    
        # Calculate total if `payment_cases` exists
        if self.payment_cases:
            self.total = Decimal(self.payment_cases.amount) * self.quantity
        
        # Save the object
        super(CartPaymentCase, self).save(*args, **kwargs)

    def __str__(self):
        return f"Cart for {self.quantity} of {self.payment_cases}"

class OrderPaymentCase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart_payment = models.OneToOneField(CartPaymentCase, on_delete=models.CASCADE)
    payment_intent_id = models.CharField(max_length=255,blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    
    # Save method override to create slug
    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(self.cart_payment.membersID)
            self.slug = unique_slug(value, type(self)) 
        super(OrderPaymentCase, self).save(*args, **kwargs)

    def __str__(self):
        return self.payment_intent_id  