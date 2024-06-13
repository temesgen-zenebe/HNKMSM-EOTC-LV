from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static  
from django.conf import settings

from blog.views import BlogDetailView, BlogListView  

app_name = 'blog' 
urlpatterns = [
    path('blogList/', BlogListView.as_view(), name='blog_list'),
    path('blog/<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
]