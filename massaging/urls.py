from django.urls import path
from .views import MassageListView,MassageDetailView

app_name = 'massaging' 

urlpatterns = [
    path('massageList/', MassageListView.as_view(), name='massage_list'),
    path('massageDetail/<slug:slug>/', MassageDetailView.as_view(), name='massage_detail'),  
]
