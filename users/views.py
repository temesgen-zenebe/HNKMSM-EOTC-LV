from django.shortcuts import render

# Create your views here.
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from allauth.account.views import PasswordChangeView

from .forms import CustomUserChangeForm


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('my-account')

class MyAccountPageView(SuccessMessageMixin,LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = CustomUserChangeForm
    template_name = 'account/my_account.html'
    success_message = 'Update Successful'

    def get_object(self):
        return self.request.user