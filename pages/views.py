from django.shortcuts import render,redirect
from django.views.generic import TemplateView,ListView,DetailView
from django.contrib import messages 
from blog.models import Blog
from events.models import Event,EventGallery, EventsCategory, PostEventImages
from payments.models import PaymentCaseLists

from django.utils import timezone
from multimedia.models import (
    BooksLibrary, Gallery, UserManual, 
    PraiseGlory, TestimonyOfSalvation, 
    ArchiveLink,SpiritualPoemSong 
)
from members.models import MembersUpdateInformation
from shopProducts.models import ShopProduct


class HomePageView(TemplateView):
    template_name = 'pages/home.html'
   
    def get(self, request, *args, **kwargs):
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
        payment_donation = PaymentCaseLists.objects.filter(category = 'donation')
        membership = MembersUpdateInformation.objects.get(user=request.user)
        print(membership.member_status)
        latest_blog = Blog.objects.order_by('-created_at')[:3]
        products = ShopProduct.objects.all().order_by('-created')

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
             #payment_donation
             'payment_donation':payment_donation,
             'products':products,
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
     
class DonationListView(ListView):
    model = PaymentCaseLists
    template_name = 'pages/donationList.html'
    context_object_name = 'payment_cases_donation_list'
    paginate_by = 6

    def get_queryset(self):
        queryset = PaymentCaseLists.objects.filter(category='donation').order_by('created')
        return queryset

  
   
class DonationCaseDetailView(DetailView): 
    model = PaymentCaseLists
    template_name = 'pages/donation_case_detail.html'  # Specify your detail view template
    context_object_name = 'donation_case'