from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone
import uuid

class Categories(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
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
            self.slug = slugify(self.title)
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
