from django.db import models
from django.conf import settings
from common.utils.text import unique_slug
from django.core.validators import FileExtensionValidator

class Massage(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_massages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_massages', limit_choices_to={'is_staff': True})
    subject = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    attachment = models.FileField(upload_to='massage_attachments/', null=True, blank=True,
                                  validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)
  
    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(self.subject)
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.subject
