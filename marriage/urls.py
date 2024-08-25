from django.urls import path
from .views import marriageSchoolWelcome,CourseListView,CourseDetailView,ResourceDetailView,submit_quiz

app_name = 'marriage' 

urlpatterns = [
    # path('marriageSchoolWelcome', marriageSchoolWelcome.as_view(), name='marriageSchool_welcome'),
    path('marriageSchoolWelcome/', marriageSchoolWelcome.as_view(), name='marriageSchool_welcome'),

    path('courses/', CourseListView.as_view(), name='course_list'),
    path('courses/<slug:slug>/', CourseDetailView.as_view(), name='course_detail'),
    #path('course/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('quiz/submit/<int:quiz_id>/', submit_quiz, name='submit_quiz'),
    path('courses/resource/<slug:slug>/', ResourceDetailView.as_view(), name='resource_detail'),
]