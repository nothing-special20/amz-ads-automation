from .models import NewsletterSignup
from datetime import datetime


def store_newsletter_signups(name, email, company):
    doc = NewsletterSignup(
            NAME=name,
            EMAIL=email,
            COMPANY=company,
            SIGNUP_DATE=datetime.now())
    doc.save()