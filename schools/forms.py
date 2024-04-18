from django import forms
from .models import QuationsAndAnswer, FAQ, FAQReader

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

class FAQReaderForm(forms.ModelForm):
    class Meta:
        model = FAQReader
        fields = ['is_satisfied']
        labels = {
            'is_satisfied': 'Are you satisfied with the answer?'
        }
       
class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['satisfaction_rating']
        labels = {
            'satisfaction_rating': 'Satisfaction Rating'
        }
        
