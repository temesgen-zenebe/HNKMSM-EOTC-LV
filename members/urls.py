from django.urls import path
from .views import MemberCreateView, MemberListView, MemberUpdateView, ChildCreateView, RelativeCreateView

app_name = 'members' 

urlpatterns = [
    path('members', MemberListView.as_view(), name='member_list'),
    path('members/create/', MemberCreateView.as_view(), name='member_create'),
    path('members/update/<int:pk>/', MemberUpdateView.as_view(), name='member_update'),
    path('child/create/', ChildCreateView.as_view(), name='child_create'),
    path('relative/create/', RelativeCreateView.as_view(), name='relative_create'),
]
