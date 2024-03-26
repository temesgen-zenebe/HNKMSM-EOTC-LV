from django.urls import path
from .views import ServicesView,SermonServicesView,SermonMediaListView, SermonMediaDetailView

app_name = 'services'

urlpatterns = [
    path('service', ServicesView.as_view(), name='service'), 
    path('sermon', SermonServicesView.as_view(), name='sermon'),
    path('sermon_media/', SermonMediaListView.as_view(), name='sermon_media_list'),
    path('sermon_media/<int:pk>/', SermonMediaDetailView.as_view(), name='sermon_media_detail'),
]
