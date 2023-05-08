from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import ProjectProposal, Vote

class ProposalListView(ListView):
    model = ProjectProposal
    template_name = 'projectVote/proposal_list.html'
    context_object_name = 'proposals'

class ProposalDetailView(DetailView):
    model = ProjectProposal
    template_name = 'projectVote/proposal_detail.html'
    context_object_name = 'proposal'

class ProposalCreateView(LoginRequiredMixin, CreateView):
    model = ProjectProposal
    template_name = 'projectVote/proposal_form.html'
    fields = ['title', 'description']
    success_url = reverse_lazy('projectVote:proposal_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ProposalUpdateView(LoginRequiredMixin, UpdateView):
    model = ProjectProposal
    template_name = 'projectVote/proposal_form.html'
    fields = ['title', 'description']

class ProposalDeleteView(LoginRequiredMixin, DeleteView):
    model = ProjectProposal
    template_name = 'projectVote/proposal_confirm_delete.html'
    success_url = reverse_lazy('projectVote:proposal_list')

@login_required
def vote(request, proposal_id):
    proposal = get_object_or_404(ProjectProposal, pk=proposal_id)
    try:
        vote = Vote.objects.get(voter=request.user, proposal=proposal)
        vote.vote = request.POST['vote']
        vote.save()
    except Vote.DoesNotExist:
        vote = Vote(voter=request.user, proposal=proposal, vote=request.POST['vote'])
        vote.save()
    return redirect('projectVote:proposal_detail', pk=proposal_id)



