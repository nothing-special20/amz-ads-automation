from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.teams.decorators import login_and_team_required
from apps.teams.helpers import get_default_team_from_request

from .functions import store_newsletter_signups

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
        store_email_for_newsletter(request)
        # return render(request, 'web/landing_page.html')
        return render(request, 'web/landing_page/index.html')

def store_email_for_newsletter(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            company = request.POST.get('company')
            store_newsletter_signups(name, email, company)
        except Exception as e:
            print('Error storing newsletter email:\t' + e)


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

def privacy_policy(request):
    return render(request, 'web/privacy_policy.html')
