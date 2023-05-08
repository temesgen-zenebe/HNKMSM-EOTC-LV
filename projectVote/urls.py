from django.urls import path
from .views import ProposalListView, ProposalDetailView, ProposalCreateView, ProposalUpdateView, ProposalDeleteView, vote

app_name = 'projectVote'

urlpatterns = [
    path('proposal_list', ProposalListView.as_view(), name='proposal_list'),
    path('<int:pk>/', ProposalDetailView.as_view(), name='proposal_detail'),
    path('new/', ProposalCreateView.as_view(), name='proposal_create'),
    path('<int:pk>/update/', ProposalUpdateView.as_view(), name='proposal_update'),
    path('<int:pk>/delete/', ProposalDeleteView.as_view(), name='proposal_delete'),
    path('<int:proposal_id>/vote/', vote, name='proposal_vote'),
]
