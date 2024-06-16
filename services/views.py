from email.mime import application
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView,UpdateView
from .models import BaptizedCertification, Sermon, SermonCategory, SermonMedia
from django.contrib.auth.models import User
from .forms import BaptizedApplicationForm, BaptizedApplicationUpdatingForm
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
    #model = BaptizedCertification
    template_name = 'services/baptism_service.html'  # Template name to be created
          
    def get(self, request):
        #Forms
        baptizedForm = BaptizedApplicationForm()
        baptizedApplicationConfirmation = BaptizedCertification.objects.filter(user=self.request.user).first()
        context = {
            'baptizedForm': baptizedForm,
            'baptizedApplicationConfirmation':baptizedApplicationConfirmation,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        baptizedForm = BaptizedApplicationForm(request.POST)
        user = request.user
        
        if baptizedForm.is_valid():
            # user = request.user
            baptized_application = baptizedForm.save(commit=False)
            baptized_application.user = user
            baptized_application.save()
            # Add a success message
            messages.success(request, 'Your baptism application has been successfully submitted!')
            return redirect('services:baptism_service')
                       
        context = {
            'baptizedForm': baptizedForm, 
        }
        return render(request, self.template_name, context)

class BaptizedApplicationUpdatingView(LoginRequiredMixin, UpdateView):
    model = BaptizedCertification
    template_name = 'services/baptism_service_ApplicationUpdating.html'
    form_class = BaptizedApplicationUpdatingForm
    success_url = reverse_lazy('services:baptism_service')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return BaptizedCertification.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Your baptism application information has been updated successfully!')
        return super().form_valid(form)

# HolyCommunion
class HolyCommunionServicesView(TemplateView):
    template_name = 'services/holyCommunion.html'
    
#Father of Repentance
class FatherOfRepentanceServicesView(TemplateView):
    template_name = 'services/fatherOfRepentance.html'

#Funeral Services 
class FuneralServicesView(TemplateView):
    template_name = 'services/funeralServicesView.html'