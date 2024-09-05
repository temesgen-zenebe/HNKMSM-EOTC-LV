from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,DetailView
from massaging.models import Massage

# Create your views here.
class MassageListView(LoginRequiredMixin, ListView):
    model = Massage
    template_name = "massaging/yourMassage.html"
    context_object_name = 'massages'
    paginate_by = 10
    
    def get_queryset(self):
        return Massage.objects.filter(recipient=self.request.user).order_by('-created')
    
class MassageDetailView(LoginRequiredMixin, DetailView):
    model = Massage
    template_name = "massaging/yourMassageDetail.html"
    context_object_name = 'massage'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        massage = self.get_object()
        context['is_pdf'] = massage.attachment.url.lower().endswith('.pdf') if massage.attachment else False
        return context