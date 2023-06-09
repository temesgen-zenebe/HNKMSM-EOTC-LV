from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static  
from django.conf import settings  
 
urlpatterns = [
    # Admin
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    
    # User Management
    path('account/', include('allauth.urls')),
    
    path('', include('pages.urls')),
    path('projectVote/', include('projectVote.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
