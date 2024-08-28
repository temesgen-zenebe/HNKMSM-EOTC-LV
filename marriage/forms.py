from django import forms
from .models import SignupForSchool ,marriageQuationsAndAnswer,SignupForMeetEvents

class SignupForSchoolForm(forms.ModelForm):
    class Meta:
        model = SignupForSchool
        fields = ['date_of_birth', 'email', 'phone', 'city', 'country', 'confirmation']

class marriageSchoolQuationsAndAnswerForm(forms.ModelForm):
    class Meta:
        model = marriageQuationsAndAnswer
        fields = ['course','question']
        widgets = {
            'course':forms.HiddenInput(),
            'question': forms.Textarea(
                attrs={'class': 'w-100 form-control form-control-sm mb-4 p-3 border-primary bg-light',
                'rows': 4, 'cols': 10, 'placeholder': "Leave your short and brief questions or comments here, and we'll respond promptly!",
                'required': True})
        }
        
