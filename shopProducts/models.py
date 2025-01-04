from django.db import models
from common.utils.text import unique_slug
from django.conf import settings

class ShopProduct(models.Model):
    CATEGORY=( ('photoFrames', 'photoFrames'),('outSourcesProducts ', 'outSourcesProducts'),('inOurStore', 'inOurStore'))
    # Product fields
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000,blank=True, null=True)
    specification = models.TextField(max_length=1000,blank=True, null=True)
    affiliate_link = models.URLField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='shop_products/', blank=True, null=True)
    rating_number = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category =models.CharField(max_length=50, choices=CATEGORY, default='inOurStore')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    seller = models.CharField(max_length=200, blank=True, null=True)
    paymentCaseCode= models.CharField(max_length=200, blank=True, null=True,
      help_text="if the produce from in OurStore than the paymentCaseCode will be slug of PaymentCases,else leave it blank")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(self.name)
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created']
        verbose_name = 'Shop Product'
        verbose_name_plural = 'Shop Products'

