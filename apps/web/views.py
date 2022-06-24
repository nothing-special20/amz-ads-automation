from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.teams.decorators import login_and_team_required
from apps.teams.helpers import get_default_team_from_request


def home(request):
    if request.user.is_authenticated:
        team = get_default_team_from_request(request)
        if team:
            return HttpResponseRedirect(reverse('web_team:home', args=[team.slug]))
        else:
            messages.info(request, _(
                'Teams are enabled but you have no teams. '
                'Create a team below to access the rest of the dashboard.'
            ))
            return HttpResponseRedirect(reverse('teams:manage_teams'))
    else:
        return render(request, 'web/landing_page.html')


@login_and_team_required
def team_home(request, team_slug):
    assert request.team.slug == team_slug
    return render(request, 'web/app_home.html', context={
        'team': request.team,
        'active_tab': 'dashboard',
        'page_title': _('%(team)s Dashboard') % {'team': request.team},
    })


def simulate_error(request):
    raise Exception('This is a simulated error.')
