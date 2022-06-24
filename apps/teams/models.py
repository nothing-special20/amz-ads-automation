import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse
from apps.subscriptions.models import SubscriptionModelBase
from apps.utils.models import BaseModel
from apps.web.meta import absolute_url

from . import roles


class Team(SubscriptionModelBase, BaseModel):
    """
    A Team, with members.
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='teams', through='Membership')

    # your team customizations go here.

    def __str__(self):
        return self.name

    @property
    def sorted_memberships(self):
        return self.membership_set.order_by('user__email')

    def pending_invitations(self):
        return self.invitations.filter(is_accepted=False)

    @property
    def dashboard_url(self):
        return reverse('web_team:home', args=[self.slug])


class Membership(BaseModel):
    """
    A user's team membership
    """
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, choices=roles.ROLE_CHOICES)
    # your additional membership fields go here.

    def __str__(self):
        return f'{self.user}: {self.team}'

    def is_admin(self) -> bool:
        return self.role == roles.ROLE_ADMIN


class Invitation(BaseModel):
    """
    An invitation for new team members.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='invitations')
    email = models.EmailField()
    role = models.CharField(max_length=100, choices=roles.ROLE_CHOICES, default=roles.ROLE_MEMBER)
    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='sent_invitations')
    is_accepted = models.BooleanField(default=False)
    accepted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='accepted_invitations', null=True, blank=True)

    def get_url(self):
        return absolute_url(reverse('teams:accept_invitation', args=[self.id]))


class BaseTeamModel(BaseModel):
    """
    Abstract model for objects that are part of a team.

    See `teams_example` app for usage.
    """
    team = models.ForeignKey(Team, verbose_name="Team", on_delete=models.CASCADE)

    class Meta:
        abstract = True
