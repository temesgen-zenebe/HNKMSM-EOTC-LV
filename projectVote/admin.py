from django.contrib import admin
from .models import ProjectProposal,Vote


@admin.register(ProjectProposal)
class ProjectProposalAdmin(admin.ModelAdmin):
    model = ProjectProposal
    list_display = ['title', 'description', 'author', 'created_at', 'updated']

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return ('created_at', 'updated')
        return ()
    

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    model = Vote
    list_display = ['voter', 'proposal', 'vote', 'created_at', 'updated']

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return ('created_at', 'updated')
        return ()