from django import forms
from .models import CartPaymentCase


class PaymentCaseCartForm(forms.ModelForm):
    class Meta:
        model = CartPaymentCase
        fields = ['quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].widget.attrs.update({
            'min': 1,  # Enforce minimum value
            'class': 'form-control form-control-sm',  # Add Bootstrap style
        })
        # self.fields['payment_case'].widget.attrs.update({
        #     'class': 'form-control form-control-sm',  # Add Bootstrap style
        # })
