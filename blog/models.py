from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
# from ckeditor.fields import RichTextField 
#    e.g content = RichTextField(blank=True, null=True)

from common.utils.text import unique_slug  # Assuming you have a utility for generating unique slugs

class BlogCategory(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self.name, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Blog(models.Model):
    VISIBILITY = [
        ('public', 'public'),
        ('private', 'private'),
    ]
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    published_at = models.DateTimeField(default=timezone.now)
    published_by = models.CharField(max_length=100, blank=True, null=True)
    visibility =models.CharField(max_length=50, default="private", choices=VISIBILITY)
    cover_image = models.ImageField(upload_to='blog/blog_covers/', blank=True, null=True)
    categories = models.ManyToManyField(BlogCategory, related_name='blogs', blank=True)
    viewerCount = models.PositiveIntegerField(default=0)  # Example field to track viewerCount
    web_link = models.URLField(blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self.title, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:blog_detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-published_at', '-created_at']