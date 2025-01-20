# events/views.py
from pyexpat.errors import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from .models import Event, EventGallery, PostEventImages,NewsAndAnnouncements,RemindMeUpcomingEvent
from django.shortcuts import get_object_or_404, redirect
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
    
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        
        # Increment the viewer count
        if obj.short_review :
            obj.viewers_count += 1
            obj.save(update_fields=['viewers_count'])  # Save only the updated field for efficiency
            
        return obj
    def get_context_data(self, **kwargs):
        # Fetch the base context from the superclass
        context = super().get_context_data(**kwargs)
        
        # Get the current EventGallery instance
        event_gallery = self.get_object()
        
        # Filter PostEventImages based on the current EventGallery instance
        context["postEvent_Images"] = PostEventImages.objects.filter(event_gallery=event_gallery)
        
        return context

# ListView for News & Announcements
class NewsAndAnnouncementsListView(ListView):
    model = NewsAndAnnouncements
    template_name = 'events/news_and_announcements_list.html'
    context_object_name = 'news_list'
    paginate_by = 10  # Adjust pagination as needed
    ordering = ['-created']  # Orders by latest first

# DetailView for News & Announcements
class NewsAndAnnouncementsDetailView(DetailView):
    model = NewsAndAnnouncements
    template_name = 'events/news_and_announcements_detail.html'
    context_object_name = 'news'

    def get_object(self):
        return get_object_or_404(NewsAndAnnouncements, slug=self.kwargs['slug'])
    
class UserNotificationListView(LoginRequiredMixin, ListView):
    model = RemindMeUpcomingEvent
    template_name = 'events/remind_me_note.html'
    context_object_name = 'remind_me_note'
    
    def get_queryset(self):
        return RemindMeUpcomingEvent.objects.filter(your_name=self.request.user, is_passed = False)
    
class AddRemindMeNotificationCreateView(LoginRequiredMixin, CreateView):
   
    def post(self, request, slug):
        # Fetch the upcoming event
        upcoming_event = get_object_or_404(Event, slug=slug)

        # Check if the RemindMeUpcomingEvent already exists
        remind_me_event, created = RemindMeUpcomingEvent.objects.get_or_create(
            event=upcoming_event,
            your_name=request.user,
        )

        # Redirect to the event list view after processing
        return redirect('events:event_list')
        