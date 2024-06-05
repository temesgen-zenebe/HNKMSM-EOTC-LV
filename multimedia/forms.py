from django import forms
from .models import BooksLibrary

class BooksLibraryForm(forms.ModelForm):
    class Meta:
        model = BooksLibrary
        fields = ['title', 'author', 'published_date', 'format_type', 'cover_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'author': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'published_date': forms.DateInput(attrs={'type': 'date','class': 'form-control form-control-sm'}),
            'format_type': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'cover_image': forms.ClearableFileInput(attrs={'class': 'form-control-file form-control-sm' ,'type':'file'}),
            }