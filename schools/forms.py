from django import forms
from .models import QuationsAndAnswer

class QuationsAndAnswerForm(forms.ModelForm):
    class Meta:
        model = QuationsAndAnswer
        fields = ['course','question']
        widgets = {
            'course':forms.HiddenInput(),
            'question': forms.Textarea(attrs={'class': 'w-100 form-control form-control-sm mb-4 p-3 border-primary bg-light',
                                              'rows': 4, 'cols': 10,
                                              'placeholder': "Leave your short and brief questions here, and we'll respond promptly!",
                                              'required': True})
        }
