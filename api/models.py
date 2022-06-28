from django.db import models

# Create your models here.
class AmzTokens(models.Model):
    PROFILE_ID = models.TextField()
    PROFILE_NAME = models.TextField()
    REFRESH_TOKEN = models.TextField()
    LAST_UPDATED = models.DateTimeField()
