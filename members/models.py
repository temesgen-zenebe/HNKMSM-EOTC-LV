from django.db import models
from django.conf import settings
from common.utils.text import unique_slug
from django.utils import timezone
import random
import string

# Create your models here.
class MembersUpdateInformation(models.Model):
    MARITAL_STATUS = (
        ('married', 'married'),
        ('single', 'single'),  
    )
    MEMBER_STATUS = (
        ('active', 'active'),
        ('pending', 'pending'),  
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    member_id = models.CharField(max_length=10, unique=True, editable=False, default='m')
    full_name = models.CharField(max_length=255)
    baptismal_name = models.CharField(max_length=255,blank=True, null=True)
    godfather = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    apartment = models.CharField(max_length=50, blank=True, null=True)
    telephone_number = models.CharField(max_length=20)
    email = models.EmailField()
    marital_status =  models.CharField(max_length=100, choices=MARITAL_STATUS)
    spouse_name = models.CharField(max_length=255, blank=True, null=True)
    spouse_baptismal_name = models.CharField(max_length=255, blank=True, null=True)
    member_status = models.CharField(max_length=100, choices=MEMBER_STATUS, default='pending')
    slug = models.SlugField(max_length=200, unique=True ,null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def generate_unique_member_id(self):
        while True:
            unique_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            if not MembersUpdateInformation.objects.filter(member_id=unique_id).exists():
                return unique_id
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(self.full_name)
            self.slug = unique_slug(value, type(self))
            
        if not self.member_id:
            self.member_id = self.generate_unique_member_id()
        
        super().save(*args, **kwargs)
        
    
    def __str__(self):
        return self.full_name

class Child(models.Model):
    GENDER = (
        ('M', 'M'),
        ('F', 'F'),  
    )
    member = models.ForeignKey(MembersUpdateInformation, related_name='children', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=20, choices=GENDER)

    def __str__(self):
        return self.name

class Relative(models.Model):
    member = models.ForeignKey(MembersUpdateInformation, related_name='relatives', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    relationship = models.CharField(max_length=100)  # e.g., brother, sister, cousin, etc.

    def __str__(self):
        return self.name