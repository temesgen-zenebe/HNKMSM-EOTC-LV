from django.db import models
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
