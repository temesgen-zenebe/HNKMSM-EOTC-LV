from django.urls import path

from .views import (AboutUsView, HomePageView, 
                    Contact, TermAndCondition,
                    UserDashboard,ChildCare, 
                    DonationListView,DonationCaseDetailView
                    )

app_name = 'pages'

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
    path('about-us/', AboutUsView.as_view(), name='about-us'),
    path('contact-us/', Contact.as_view(), name='contact-us'),
    path('terms-polices/', TermAndCondition.as_view(), name='terms-polices'),
    path('user-dashboard/', UserDashboard.as_view(), name='user-dashboard'),
    path('childcare/', ChildCare.as_view(), name='childcare'),
    path('donationCaseList/', DonationListView.as_view(), name='donation-caseList'),
    path('donationCaseDetail/<slug:slug>/', DonationCaseDetailView.as_view(), name='donation-detail'),
]