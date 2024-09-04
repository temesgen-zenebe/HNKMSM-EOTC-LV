from django.views.generic import DetailView,ListView
from .models import ShopProduct

# class ShopProductListView(ListView):
#     model = ShopProduct
#     template_name = 'shopProducts/shopProductList.html'
#     context_object_name = 'products'

from django.views.generic import ListView
from django.db.models import Q

class ShopProductListView(ListView):
    model = ShopProduct
    template_name = 'shopProducts/shopProductList.html'
    context_object_name = 'products'
    paginate_by = 9  # Adjust the number as needed

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_category'] = self.request.GET.get('category', '')
        return context


class ShopProductDetailView(DetailView):
    model = ShopProduct
    template_name = 'shopProducts/shopProductDetail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        related_products = ShopProduct.objects.filter(category=self.object.category).exclude(id=self.object.id)[:4]
        context['related_products'] = related_products
        return context