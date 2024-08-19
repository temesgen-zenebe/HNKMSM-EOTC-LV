from django.urls import path
from .views import marriageSchoolWelcome,CourseListView,CourseDetailView

app_name = 'marriage' 

urlpatterns = [
    path('marriageSchoolWelcome', marriageSchoolWelcome.as_view(), name='marriageSchool_welcome'),
    path('courses/', CourseListView.as_view(), name='course_list'),
    path('courses/<slug:slug>/', CourseDetailView.as_view(), name='course_detail'),
]