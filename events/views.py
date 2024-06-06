# events/views.py
from django.views.generic import ListView, DetailView
from .models import Event, EventGallery
from django.utils import timezone

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 10  # Optional: Add pagination
    
    def get_queryset(self):
        now = timezone.now()
        queryset = super().get_queryset()
        
        for event in queryset:
            if event.end_time < now and event.status_tag != 'past':
                event.status_tag = 'past'
                event.save()
            elif event.end_time >= now and event.status_tag != 'active':
                event.status_tag = 'active'
                event.save()
        
        for event in queryset:
            if event.end_time < now and event.status_tag == 'past':
               
                # Check if an EventGallery entry with the same post_events and held_date already exists
                if not EventGallery.objects.filter(post_events=event, held_date=event.end_time.date()).exists():
                    # Create a new EventGallery object
                    EventGallery.objects.create(
                        post_events=event,
                        number_of_participants=event.max_number_guests,
                        held_date=event.end_time,  # Ensure held_date is a date object
                        category=event.category,
                        thumbnail_title=event.title  # Assuming you want to use the event title as the thumbnail title
                    )
                
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_events"] = Event.objects.filter(status_tag='active')
        return context

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
