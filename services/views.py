from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from .models import SermonMedia

class ServicesView(TemplateView):
    template_name = 'services/servicesView.html'

class SermonServicesView(TemplateView):
    template_name = 'services/sermon.html'
    

class SermonMediaListView(ListView):
    model = SermonMedia
    template_name = 'services/sermon_media_list.html'  # Template name to be created
    context_object_name = 'sermon_media_list'

class SermonMediaDetailView(DetailView):
    model = SermonMedia
    template_name = 'services/sermon_media_detail.html'  # Template name to be created
    context_object_name = 'sermon_media'
