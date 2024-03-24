from django.urls import path
from .views import ServicesView,SermonServicesView

app_name = 'services'

urlpatterns = [
    path('service', ServicesView.as_view(), name='service'), 
    path('sermon', SermonServicesView.as_view(), name='sermon'),
]