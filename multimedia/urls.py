from django.urls import path
from .views import (
    BooksLibraryListView, BooksLibraryDetailView,
    GalleryListView, GalleryDetailView,
    UserManualListView, UserManualDetailView,
    PraiseGloryListView, PraiseGloryDetailView,
    TestimonyOfSalvationListView, TestimonyOfSalvationDetailView,
    ArchiveLinkListView, ArchiveLinkDetailView
)
app_name = 'multimedia'

urlpatterns = [
    path('books/', BooksLibraryListView.as_view(), name='books_library_list'),
    path('books/<slug:slug>/', BooksLibraryDetailView.as_view(), name='books_library_detail'),
    path('gallery/', GalleryListView.as_view(), name='gallery_list'),
    path('gallery/<slug:slug>/', GalleryDetailView.as_view(), name='gallery_detail'),
    path('manuals/', UserManualListView.as_view(), name='user_manual_list'),
    path('manuals/<slug:slug>/', UserManualDetailView.as_view(), name='user_manual_detail'),
    path('praises/', PraiseGloryListView.as_view(), name='praise_glory_list'),
    path('praises/<slug:slug>/', PraiseGloryDetailView.as_view(), name='praise_glory_detail'),
    path('testimonies/', TestimonyOfSalvationListView.as_view(), name='testimony_of_salvation_list'),
    path('testimonies/<slug:slug>/', TestimonyOfSalvationDetailView.as_view(), name='testimony_of_salvation_detail'),
    path('archives/', ArchiveLinkListView.as_view(), name='archive_link_list'),
    path('archives/<slug:slug>/', ArchiveLinkDetailView.as_view(), name='archive_link_detail'),
]
