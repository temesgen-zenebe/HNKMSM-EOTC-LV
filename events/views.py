# events/views.py
from django.views.generic import ListView, DetailView
from .models import Event, EventGallery

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 10  # Optional: Add pagination

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

class EventGalleryListView(ListView):
    model = EventGallery
    template_name = 'events/event_gallery_list.html'
    context_object_name = 'galleries'
    paginate_by = 10  # Optional: Add pagination

class EventGalleryDetailView(DetailView):
    model = EventGallery
    template_name = 'events/event_gallery_detail.html'
    context_object_name = 'gallery'
