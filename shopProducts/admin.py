from django.contrib import admin
from .models import *

@admin.register(ShopProduct)
class ShopProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'affiliate_link','rating_number','price','created_by','seller')
    search_fields = ('name','seller')