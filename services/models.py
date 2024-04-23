from django.db import models
from django.conf import settings
from common.utils.text import unique_slug

# Sermon services
class SermonSeries(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # Add any other fields relevant to sermon series
    
    def __str__(self):
        return self.title
    
class SermonCategory(models.Model):
    category = models.CharField(max_length=200)
    subcategory = models.CharField(max_length=200)
    # Add any other fields relevant to sermon series
    
    def __str__(self):
        return self.category

class Sermon(models.Model):
    title = models.CharField(max_length=200)
    preacher = models.CharField(max_length=100)
    date_preached = models.DateField()
    series = models.ForeignKey(SermonSeries, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(SermonCategory, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='sermonGallery/%Y/%m/%d', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True ,null=True, blank=True)  # Add this line
    
    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(self.title)
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class SermonMedia(models.Model):
    SERMON_TYPES = (
        ('audio', 'Audio'),
        ('video', 'Video'),
        ('transcript', 'Transcript'),
    )
    sermon = models.ForeignKey(Sermon, on_delete=models.CASCADE)
    media_type = models.CharField(max_length=20, choices=SERMON_TYPES)
    media_url = models.URLField()
    # Add any other fields relevant to sermon media
    
class Comment(models.Model):
    sermon = models.ForeignKey(Sermon, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField(default="God is great!!")
    respond = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    respond_at = models.DateTimeField(auto_now=True)
    # Add any other fields relevant to comments
    
    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(self.user)
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.comment