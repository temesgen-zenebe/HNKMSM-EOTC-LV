from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView

# Create your views here.
class SchoolsView(TemplateView):
    template_name = 'schools/schoolsView.html'
class SchoolsYouthSchool(TemplateView):
    template_name = 'schools/youthSchool.html'
class SchoolsChildrenSchool(TemplateView):
    template_name = 'schools/childrenSchool.html'