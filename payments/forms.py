from django import forms
from .models import BillingInformation, PaymentCaseCartList

class BillingForm(forms.ModelForm):
    payment_case = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = BillingInformation
        fields = ['address', 'city', 'state', 'postal_code', 'country', 'payment_case']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from the kwargs
        super(BillingForm, self).__init__(*args, **kwargs)
        
        if user:
            # Determine the payment_case value based on the user's cart
            payment_case = None
            cart_list = PaymentCaseCartList.objects.filter(user=user)
            for cart_item in cart_list:
                if cart_item.payment_case.category.title.lower() == 'membership':
                    payment_case = 'membership'
                    break
            
            self.fields['payment_case'].initial = payment_case

class CardInformationForm(forms.Form):
    card_number = forms.CharField(max_length=16, min_length=16, widget=forms.NumberInput(attrs={'placeholder': 'Card Number'}))
    expiry_date = forms.CharField(max_length=5, widget=forms.TextInput(attrs={'placeholder': 'MM/YY'}))
    cvc = forms.CharField(max_length=4, widget=forms.NumberInput(attrs={'placeholder': 'CVC'}))
