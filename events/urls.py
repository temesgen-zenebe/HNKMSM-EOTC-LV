# events/urls.py
from django.urls import path
from .views import (
    EventListView, EventDetailView, 
    EventGalleryListView, EventGalleryDetailView,
    NewsAndAnnouncementsListView, 
    NewsAndAnnouncementsDetailView
    )

app_name = 'events' 

urlpatterns = [
    path('events', EventListView.as_view(), name='event_list'),
    path('event/<slug:slug>/', EventDetailView.as_view(), name='event_detail'),
    path('galleries/', EventGalleryListView.as_view(), name='event_gallery_list'),
    path('gallery/<slug:slug>/', EventGalleryDetailView.as_view(), name='event_gallery_detail'),
    path('NewsAndAnnouncements/', NewsAndAnnouncementsListView.as_view(), name='NewsAndAnnouncements_list'),
    path('NewsAndAnnouncements/<slug:slug>/', NewsAndAnnouncementsDetailView.as_view(), name='NewsAndAnnouncements_detail'),
]
