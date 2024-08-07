from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages 
from blog.models import Blog
from events.models import Event,EventGallery, EventsCategory, PostEventImages
from django.utils import timezone
from multimedia.models import (
    BooksLibrary, Gallery, UserManual, 
    PraiseGlory, TestimonyOfSalvation, 
    ArchiveLink,SpiritualPoemSong 
)
from members.models import MembersUpdateInformation


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
        
        #Multimedia
        latest_archives = ArchiveLink.objects.order_by('-created_at')[:3]
        latest_booksLibraries = BooksLibrary.objects.order_by('-created_at')[:3]
        latest_gallery = Gallery.objects.order_by('-uploaded_at')[:3]
        latest_praiseGlory = PraiseGlory.objects.order_by('-created_at')[:3]
        latest_spiritualPoemSongs = SpiritualPoemSong.objects.order_by('-created_at')[:3]
        latest_testimonySalvations = TestimonyOfSalvation.objects.order_by('-created')[:3]
        latest_userManuals = UserManual.objects.order_by('-uploaded_at')[:3]
        #membership
        membership = MembersUpdateInformation.objects.filter(user=self.request.user)
        #BLOG
        latest_blog = Blog.objects.order_by('-created_at')[:3]
     

        context = {
             #membership
             'membership' : membership,
             'event': events,
             'eventGallery':eventGallery,
             'eventsCategory':eventsCategory,
             'postEventImages':postEventImages,
             
              #Multimedia
             'latest_archives' : latest_archives,
             'latest_booksLibraries' : latest_booksLibraries,
             'latest_gallery' :  latest_gallery,
             'latest_praiseGlory' :  latest_praiseGlory,
             'latest_spiritualPoemSongs' : latest_spiritualPoemSongs,
             'latest_testimonySalvations' : latest_testimonySalvations,
             'latest_userManuals' :  latest_userManuals,
             'latest_blog' : latest_blog,
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
    
    