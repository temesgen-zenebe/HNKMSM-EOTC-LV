from email.mime import application
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from .models import Sermon, SermonCategory, SermonMedia
from .forms import BaptizedApplicationForm
class ServicesView(TemplateView):
    template_name = 'services/servicesView.html'

class SermonServicesView(TemplateView):
    template_name = 'services/sermon.html'
    
class SermonMediaListView(ListView):
    model = SermonMedia
    template_name = 'services/sermon_media_list.html'  # Template name to be created
    context_object_name = 'sermon_media_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sermon_media = SermonMedia.objects.all() 
        context['sermon_categories'] = {}

        for media in sermon_media:
            category = media.sermon.category.category
            if category not in context['sermon_categories']:
                context['sermon_categories'][category] = SermonCategory.objects.filter(category=category)

        return context

                
class SermonMediaDetailView(DetailView):
    model = SermonMedia
    template_name = 'services/sermon_media_detail.html'  # Template name to be created
    context_object_name = 'sermon_media'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sermon_media = self.get_object()  # Get the current SermonMedia object
        related_sermons = Sermon.objects.filter(category=sermon_media.sermon.category)  # Filter related sermons by category

        context['related_sermons'] = related_sermons
        return context

class BaptismServiceView(LoginRequiredMixin,View):
    # model = SermonMedia
    template_name = 'services/baptism_service.html'  # Template name to be created
    def get(self, request):
        baptizedForm = BaptizedApplicationForm()
        context = {'baptizedForm': baptizedForm}
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = BaptizedApplicationForm(request.POST)
        if form.is_valid():
            user = request.user
            baptized_application = form.save(commit=False)
            baptized_application.user = user
            baptized_application.save()
            # Add a success message
            messages.success(request, 'Your baptism application has been successfully submitted!')
            return redirect('services:baptism_service')
        else:
            context = {'baptizedForm': form}
            return render(request, self.template_name, context)