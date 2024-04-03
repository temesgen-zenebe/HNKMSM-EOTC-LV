from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.views import View
from .models import Course, Chapter, Quiz, Question, Answer, Result, Report

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
        courses = Course.objects.all()
        chapter = Chapter.objects.all()
        context = {
            'courses': courses,
            'chapters': chapter,
            }
        return render(request, self.template_name, context)
    
    def post(self, request):
        context={}
        return render(request, self.template_name, context)
        
    
     