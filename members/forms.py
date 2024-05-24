from django import forms
from django.forms import inlineformset_factory
from .models import MembersUpdateInformation, Child, Relative

class MembersUpdateInformationForm(forms.ModelForm):
    marital_status = forms.ChoiceField(
        choices=MembersUpdateInformation.MARITAL_STATUS, 
        widget=forms.RadioSelect
    )

    class Meta:
        model = MembersUpdateInformation
        fields = [
            'full_name', 'baptismal_name', 'godfather', 'address', 'city', 
            'state', 'zip_code', 'apartment', 'telephone_number', 'email', 
            'marital_status', 'spouse_name', 'spouse_baptismal_name',
            'how_mony_children','how_mony_relatives'
        ]
    

ChildFormSet = inlineformset_factory(MembersUpdateInformation, Child, fields=('name','age','gender'), extra=1, can_delete=True)
RelativeFormSet = inlineformset_factory(MembersUpdateInformation, Relative, fields=('name', 'relationship'), extra=1, can_delete=True)
