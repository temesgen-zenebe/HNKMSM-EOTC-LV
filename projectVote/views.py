from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.http import JsonResponse
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
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proposal = self.object

        # Count votes for each VOTE_CHOICES option
        vote_counts = proposal.vote_set.values('vote').annotate(count=Count('id'))

        # Convert vote_counts to a list of dictionaries
        votes_data = []
        for vote_count in vote_counts:
            vote = dict()
            vote['vote'] = vote_count['vote']
            vote['count'] = vote_count['count']
            votes_data.append(vote)

        # Add votes_data to the context
        context['votes_data'] = votes_data 

        return context

    def post(self, request, *args, **kwargs):
        proposal = self.get_object()
        vote = request.POST.get('vote')

        # Check if user has already voted
        has_voted = proposal.vote_set.filter(voter=request.user).exists()

        # If user has not voted, create a new Vote object
        if not has_voted:
            Vote.objects.create(voter=request.user, proposal=proposal, vote=vote)

        # If user has voted, update the existing Vote object
        else:
            existing_vote = proposal.vote_set.get(voter=request.user)
            existing_vote.vote = vote
            existing_vote.save()

        # Redirect to the same page to display the updated vote counts
        return JsonResponse({'success': True})

class ProposalCreateView(LoginRequiredMixin, CreateView):
    model = ProjectProposal
    template_name = 'projectVote/proposal_form.html'
    fields = ['title', 'description','image']
    success_url = reverse_lazy('projectVote:proposal_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ProposalUpdateView(LoginRequiredMixin, UpdateView):
    model = ProjectProposal
    fields = ['title', 'description', 'image']
    template_name = "projectVote/proposal_form_update.html"
   
    success_url = reverse_lazy('projectVote:proposal_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

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



