from django.urls import path
from .views import ShopProductDetailView, ShopProductListView

app_name = 'shopProducts' 

urlpatterns = [
    path('products/', ShopProductListView.as_view(), name='shop_product_list'),
    path('product/<slug:slug>/', ShopProductDetailView.as_view(), name='shop_product_detail'),
]