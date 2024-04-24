from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from .models import Sermon, SermonCategory, SermonMedia

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
