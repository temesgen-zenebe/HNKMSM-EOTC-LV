from django.urls import path
from .views import SchoolsView, SchoolsYouthSchool, SchoolsChildrenSchool

app_name = 'schools' 

urlpatterns = [
    path('schools', SchoolsView.as_view(), name='school'), 
    path('youthSchool', SchoolsYouthSchool.as_view(), name='youthSchool'), 
    path('childrenSchool', SchoolsChildrenSchool.as_view(), name='childrenSchool'), 
]