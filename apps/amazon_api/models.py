from django.db import models

# Create your models here.
class AmzTokens(models.Model):
    USER = models.TextField()
    PROFILE_ID = models.TextField()
    PROFILE_NAME = models.TextField()
    REFRESH_TOKEN = models.TextField()
    LAST_UPDATED = models.DateTimeField()

class AmzScheduledReports(models.Model):
    USER = models.TextField()
    PROFILE_ID = models.TextField()
    REPORT_ENDPOINT = models.TextField(default='_')
    REPORT_ID = models.TextField()
    REPORT_DATE = models.IntegerField()
    GOOGLE_SHEET_ID = models.TextField()
    DATE_SCHEDULED = models.DateTimeField()