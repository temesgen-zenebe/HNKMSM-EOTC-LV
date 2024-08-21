from django.urls import path
from .views import marriageSchoolWelcome,CourseListView,CourseDetailView,ResourceDetailView

app_name = 'marriage' 

urlpatterns = [
    path('marriageSchoolWelcome', marriageSchoolWelcome.as_view(), name='marriageSchool_welcome'),
    path('courses/', CourseListView.as_view(), name='course_list'),
    path('courses/<slug:slug>/', CourseDetailView.as_view(), name='course_detail'),
    path('courses/resource/<slug:slug>/', ResourceDetailView.as_view(), name='resource_detail'),
]