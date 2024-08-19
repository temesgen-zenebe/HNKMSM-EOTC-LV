from django import forms
from .models import SignupForSchool

class SignupForSchoolForm(forms.ModelForm):
    class Meta:
        model = SignupForSchool
        fields = ['date_of_birth', 'email', 'phone', 'city', 'country', 'confirmation']
