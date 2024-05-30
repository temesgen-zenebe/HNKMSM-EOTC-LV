from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages 
from events.models import Event,EventGallery, EventsCategory, PostEventImages
from django.utils import timezone


class HomePageView(TemplateView):
    template_name = 'pages/home.html'
   
    def get(self, request):
        # Get the current time to filter out past events
        now = timezone.now()
        # Query the latest three upcoming events
        events = Event.objects.filter(start_time__gt=now).order_by('-start_time')[:3]
        eventGallery = EventGallery.objects.all().order_by('-created')
        eventsCategory = EventsCategory.objects.all()
        postEventImages = PostEventImages.objects.all()
        context = {
             'event': events,
             'eventGallery':eventGallery,
             'eventsCategory':eventsCategory,
             'postEventImages':postEventImages
          }
        return render(request, self.template_name, context)
   
class AboutUsView(TemplateView):
    template_name = 'pages/about.html'

    def get(self, request, *args, **kwargs):
        messages.debug(request, 'Debug message.')
        messages.info(request, 'Info message.')
        messages.success(request, 'Success message.')
        messages.warning(request, 'Warning message.')
        messages.error(request, 'Error message.')
        return super().get(request, args, kwargs)
   
class Contact(TemplateView):
     template_name = 'pages/contact.html'
     
class TermAndCondition(TemplateView):
     template_name = 'pages/termAndCondition.html'
     
class UserDashboard(TemplateView):
     template_name = 'pages/userDashboard.html' 
     
class ChildCare(TemplateView):
     template_name = 'pages/childCare.html'
    
    