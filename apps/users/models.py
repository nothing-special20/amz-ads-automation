import hashlib

from django.contrib.auth.models import AbstractUser
from django.db import models

from djstripe.models import Customer


class CustomUser(AbstractUser):
    """
    Add additional fields to the user model here.
    """
    avatar = models.FileField(upload_to='profile-pictures/', blank=True)
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.get_full_name()} <{self.email or self.username}>'

    def get_display_name(self):
        if self.get_full_name().strip():
            return self.get_full_name()
        return self.email or self.username

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return 'https://www.gravatar.com/avatar/{}?s=128&d=identicon'.format(self.gravatar_id)

    @property
    def gravatar_id(self):
        # https://en.gravatar.com/site/implement/hash/
        return hashlib.md5(self.email.lower().strip().encode('utf-8')).hexdigest()
