from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import MembersUpdateInformation, Child, Relative
from .forms import MembersUpdateInformationForm, ChildFormSet, RelativeFormSet

class MemberCreateView(CreateView):
    model = MembersUpdateInformation
    form_class = MembersUpdateInformationForm
    template_name = 'members/member_form.html'
    success_url = reverse_lazy('members:member_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['children'] = ChildFormSet(self.request.POST)
            data['relatives'] = RelativeFormSet(self.request.POST)
        else:
            data['children'] = ChildFormSet()
            data['relatives'] = RelativeFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        children = context['children']
        relatives = context['relatives']
        self.object = form.save()
        if children.is_valid() and relatives.is_valid():
            children.instance = self.object
            children.save()
            relatives.instance = self.object
            relatives.save()
        return super().form_valid(form)


class MemberListView(LoginRequiredMixin, ListView):
    model = MembersUpdateInformation
    template_name = 'members/member_list.html'
    context_object_name = 'members'
    
    def get_queryset(self):
        return MembersUpdateInformation.objects.filter(user=self.request.user)
    
class MemberUpdateView(LoginRequiredMixin, UpdateView):
    model = MembersUpdateInformation
    form_class = MembersUpdateInformationForm
    template_name = 'members/member_form.html'
    success_url = reverse_lazy('members:member_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['children'] = ChildFormSet(self.request.POST, instance=self.object)
            data['relatives'] = RelativeFormSet(self.request.POST, instance=self.object)
        else:
            data['children'] = ChildFormSet(instance=self.object)
            data['relatives'] = RelativeFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        children = context['children']
        relatives = context['relatives']
        self.object = form.save()
        if children.is_valid() and relatives.is_valid():
            children.instance = self.object
            children.save()
            relatives.instance = self.object
            relatives.save()
        return super().form_valid(form)
