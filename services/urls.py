from django.urls import path
from .views import (
    BaptizedApplicationUpdatingView, 
    ServicesView,HolyCommunionServicesView, 
    SermonServicesView,
    SermonMediaListView, 
    SermonMediaDetailView,
    BaptismServiceView,
    FuneralServicesView,
    WeddingServicesView,
    FatherOfRepentanceListView, 
    FatherOfRepentanceDetailView
    )

app_name = 'services' 

urlpatterns = [
    path('service/', ServicesView.as_view(), name='service'), 
    path('holyCommunion/', HolyCommunionServicesView.as_view(), name='holyCommunion'),
    path('fatherOfRepentance/', FatherOfRepentanceListView.as_view(), name='fatherOfRepentance'),
    path('fathers/<slug:slug>/', FatherOfRepentanceDetailView.as_view(), name='father_of_repentance_detail'),
    path('funeralServices/', FuneralServicesView.as_view(), name='funeralServices'),
    path('weddingServices/', WeddingServicesView.as_view(), name='weddingServices'),
    path('sermon/', SermonServicesView.as_view(), name='sermon'),
    path('sermon_media/', SermonMediaListView.as_view(), name='sermon_media_list'),
    path('sermon_media/<int:pk>/', SermonMediaDetailView.as_view(), name='sermon_media_detail'),
    path('baptism_service/', BaptismServiceView.as_view(), name='baptism_service'),
    path('baptism_service/update/<slug:slug>/', BaptizedApplicationUpdatingView.as_view(), name='baptizedApplicationUpdating'),
]
