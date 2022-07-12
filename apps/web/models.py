from django.db import models

class NewsletterSignup(models.Model):
    NAME = models.TextField()
    EMAIL = models.TextField()
    COMPANY = models.TextField()
    SIGNUP_DATE = models.DateTimeField()
