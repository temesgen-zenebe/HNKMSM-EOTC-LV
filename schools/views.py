from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.views import View
from .models import Course, Chapter, Quiz, Question, Answer, Resources, Result, Report

# Create your views here.
class SchoolsView(TemplateView):
    template_name = 'schools/schoolsView.html'
    
# class SchoolsYouthSchool(TemplateView):
#     template_name = 'schools/youthSchool.html'
    
class SchoolsChildrenSchool(TemplateView):
    template_name = 'schools/childrenSchool.html'
    
class SchoolsYouthSchool(LoginRequiredMixin,View):
    template_name = 'schools/youthSchool.html'
    
    def get(self, request):
        courses = Course.objects.all().order_by('created_at')
        chapters = Chapter.objects.all().order_by('created_at')
        chapters_with_resources = []
                    
        for chapter in chapters:
            resources = Resources.objects.filter(chapter=chapter)
            chapters_with_resources.append({'chapter': chapter, 'resources': resources})
                       
        context = {
            'chapters_with_resources': chapters_with_resources, 
            'courses': courses,
            'chapters': chapters,
            }
        return render(request, self.template_name, context)
    
    def post(self, request):
        context={}
        return render(request, self.template_name, context)
        
    
     