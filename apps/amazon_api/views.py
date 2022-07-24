from django.urls import path
from django.views.generic import TemplateView

from django.conf.urls import url
from django.shortcuts import render



from .tasks import set_up_new_user

app_name = 'api'

def handle_login(request):
    url = request.build_absolute_uri()
    user = request.user.username

    if request.method == 'GET':
        set_up_new_user(url, user)

    return render(request, 'web/app_home.html', context={
        'team': 'fixthis',
        'active_tab': 'dashboard',
        'page_title': ('fixthis Dashboard') % {'team': 'fixthis'},
    })