from django.urls import path

from .views import AboutUsView, HomePageView, Contact, TermAndCondition

app_name = 'pages'

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
    path('about-us/', AboutUsView.as_view(), name='about-us'),
    path('contact-us/', Contact.as_view(), name='contact-us'),
    path('terms-polices/', TermAndCondition.as_view(), name='terms-polices'),
    #path('Contact-us/', Contact.as_view(), name='Contact-us'),
]