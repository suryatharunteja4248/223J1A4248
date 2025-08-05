from django.db import models

class ShortURL(models.Model):
    original_url = models.URLField()
    shortcode = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_minutes = models.IntegerField(default=30)

class Click(models.Model):
    short_url = models.ForeignKey(ShortURL, related_name='clicks', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    referrer = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
