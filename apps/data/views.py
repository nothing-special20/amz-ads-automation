import os
import sys
import inspect
import pandas as pd
import json

import django
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string

def index(request):
    if request.user.is_authenticated:
        return render(request, 'analytics/index.html')

    else:
        return render(request, 'subscriptions/subscription_required.html')