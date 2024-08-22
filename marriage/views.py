from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, DetailView,TemplateView
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
        user = self.request.user
        
        # Create a dictionary of course: result pairs
        context['results'] = {course: Results.objects.filter(user=user, course=course).first() for course in context['courses']}
        
        context['resources'] = Resources.objects.all()
        return context
    
class CourseDetailView(LoginRequiredMixin, DetailView): 
    model = Course
    template_name = 'marriage/course_detail.html'  # Specify your detail view template
    context_object_name = 'course_detail'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()  # Get the current course object
        context['quizzes'] = Quiz.objects.filter(course=course)
        context['questions'] = Question.objects.filter(course=course)
        context['answers'] = Answer.objects.filter(question__course=course)
        return context
    
class ResourceDetailView(LoginRequiredMixin, DetailView):
    model = Resources
    template_name = 'marriage/resources_detail.html'  # Specify your detail view template
    context_object_name = 'resources_detail'
    


@login_required
def submit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    course = quiz.course
    total_questions = Question.objects.filter(quiz=quiz).count()
    correct_answers = 0

    if request.method == 'POST':
        for question in quiz.question_set.all():
            selected_answer_id = request.POST.get(f'question_{question.id}')
            if selected_answer_id:
                selected_answer = get_object_or_404(Answer, id=selected_answer_id)
                if selected_answer.is_correct:
                    correct_answers += 1

        score = (correct_answers / total_questions) * 5  # Scale to a score out of 5
        result, created = Results.objects.get_or_create(user=request.user, quiz=quiz, course=course)
        result.score = score
        result.save()

        return redirect('marriage:course_detail', slug=course.slug)

    return render(request, 'marriage/course_detail.html', {'course_detail': course})
