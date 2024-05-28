from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages 
from events.models import Event


class HomePageView(TemplateView):
    template_name = 'pages/home.html'
   
    
    def get(self, request):
        event = Event.objects.all().order_by('created')
        context={'event':event}
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
    
    