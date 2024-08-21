from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import (Course, Quiz, Question, 
                     Answer, Results, Resources, 
                     SchoolProgressController,
                     Certification,MeetEvents,
                     SignupForSchool,SignupForMeetEvents
                )
from .forms import SignupForSchoolForm


# marriage School Welcome
class marriageSchoolWelcome(TemplateView):
    template_name = 'marriage/marriageView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['schoolProgressController'] = get_object_or_404(SchoolProgressController, user=user)
        context['results'] = get_object_or_404(Results, user=user)
        context['certification'] = get_object_or_404(Certification, user=user)
        context['meetEvents'] = MeetEvents.objects.filter(user=user) 
        
        # Instantiate the signup form
        context['signupForSchoolForm'] = SignupForSchoolForm()

        return context

    def post(self, request, *args, **kwargs):
        form = SignupForSchoolForm(request.POST)
        SchoolProgress, created = SchoolProgressController.objects.get_or_create(user=self.request.user)
        if form.is_valid():
            signup = form.save(commit=False)
            signup.user = request.user
            signup.save()
            
            # Update SchoolProgressController
            SchoolProgress.is_signup_for_school = True
            SchoolProgress.save()
            
            return redirect('marriage:marriageSchool_welcome')

        context = self.get_context_data(**kwargs)
        context['signupForSchoolForm'] = form
        return self.render_to_response(context)
    

class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'marriage/course_list.html'
    context_object_name = 'courses'
    paginate_by = 6  # Number of courses per page
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resources'] = Resources.objects.all()
        return context
    
class CourseDetailView(LoginRequiredMixin, DetailView): 
    model = Course
    template_name = 'marriage/course_detail.html'  # Specify your detail view template
    context_object_name = 'course_detail'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()  # Get the current course object
        context['quiz'] = Quiz.objects.filter(course=course)
        context['question'] = Question.objects.filter(course=course)
        context['answer'] = Answer.objects.filter(question__course=course)
        return context
    
class ResourceDetailView(LoginRequiredMixin, DetailView):
    model = Resources
    template_name = 'marriage/resources_detail.html'  # Specify your detail view template
    context_object_name = 'resources_detail'