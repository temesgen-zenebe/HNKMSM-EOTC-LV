from django import forms
from .models import BaptizedCertification

class BaptizedApplicationForm(forms.ModelForm):
    class Meta:
        model = BaptizedCertification
        fields = [
            'baptize_type',
            'baptism_date',
            'given_full_name', 
            'baptism_date', 
            'fathers_full_name', 
            'mothers_full_name', 
            'phone_number' ,
            'child_country_of_birth', 
            'christian_fathers_or_mothers_name', 
            ]
        widgets = {
            'baptism_date': forms.DateInput(attrs={'type': 'date'}),
        }
