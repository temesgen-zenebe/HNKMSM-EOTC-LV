# events/models.py
from django.db import models
from django.conf import settings
from common.utils.text import unique_slug
from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status_tag = models.CharField(max_length=200, default='active')
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='events/%Y/%m/%d', blank=True, null=True)
    media_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey('EventsCategory', on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    special_guests = models.CharField(max_length=200, blank=True, null=True)
    notices = models.TextField(blank=True, null=True)
    max_number_guests = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-start_time', '-created']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self.title, Event)
        now = timezone.now()
        
        if self.end_time < now:
            self.status_tag = 'past'
        else:
            self.status_tag = 'active'
       
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class EventsCategory(models.Model):
    name = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class EventGallery(models.Model):
    post_events = models.ForeignKey('Event', on_delete=models.SET_NULL, null=True, blank=True)
    thumbnail_title = models.CharField(max_length=200, blank=True, null=True)
    short_review = models.TextField(max_length=1000,blank=True, null=True )
    video_url = models.URLField(blank=True, null=True)
    number_of_participants = models.PositiveIntegerField(default=100)
    held_date = models.DateField()
    thumbnail_image = models.ImageField(upload_to='event_gallery/thumbnails/%Y/%m/%d', blank=True, null=True)
    viewers_count = models.PositiveIntegerField(default=0)
    category = models.ForeignKey('EventsCategory', on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-held_date', '-created']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self.thumbnail_title, EventGallery)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.thumbnail_title

class PostEventImages(models.Model):
    event_gallery = models.ForeignKey(EventGallery, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='event_gallery/images/%Y/%m/%d')

    def __str__(self):
        return f"Image for {self.event_gallery.thumbnail_title}"
    
