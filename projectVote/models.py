from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class ProjectProposal(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='project/%Y/%m/%d', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title 
    
    def get_absolute_url(self):
        return reverse('proposal_detail', args=[str(self.id)])


class Vote(models.Model):
    VOTE_CHOICES = (
        ('LIKE', 'Like'),
        ('SUPPORT', 'I support'),
        ('UNLIKE', 'Unlike'),
        ('UNSURE', 'Unsure'),
        ('CONTACT', 'Contact Us'),
    )
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    proposal = models.ForeignKey(ProjectProposal, on_delete=models.CASCADE)
    vote = models.CharField(max_length=10, choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    