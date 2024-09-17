from django.db import models
from django.conf import settings
from django.forms import ValidationError
from common.utils.text import unique_slug
from django.utils import timezone
from ckeditor.fields import RichTextField
import uuid

class Categories(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self.title, type(self))
        super(Categories, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class PaymentCase(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='payment_cases')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    case_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    imag = models.ImageField(upload_to='img/paymentCase', blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Save method override to create slug
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self.title, type(self))
        super(PaymentCase, self).save(*args, **kwargs)

    # String representation
    def __str__(self):
        return self.title

class BillingInformation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}'s Billing Information"

class PaymentCaseCartList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment_case = models.ForeignKey('PaymentCase', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.payment_case.title}"

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    billing_info = models.ForeignKey(BillingInformation, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_case = models.CharField(blank=True, null=True)
    payment_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.payment_id} by {self.user}"




class PaymentHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment_email = models.EmailField(blank=True, null=True)
    paymentConfirmation = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_case = models.ForeignKey('PaymentCaseLists', on_delete=models.CASCADE)
    payment_date = models.DateTimeField(editable=False)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True)

   
    # Save method override to create slug
    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(self.payment_case)
            self.slug = unique_slug(value, type(self))
        super(PaymentHistory, self).save(*args, **kwargs)
        
    def __str__(self):
        return f"Payment of {self.amount} by {self.user.username}"

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

    def __str__(self):
        return self.title
