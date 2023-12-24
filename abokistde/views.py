from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.core.exceptions import ValidationError

from .models import Episode, PublishingChannel, UserSubscription
from django.contrib.auth.models import User
from django.contrib.auth import password_validation, authenticate, login, logout

from django.forms.models import model_to_dict
import json

from datetime import datetime, timedelta, timezone

import uuid

from django.views.decorators.csrf import csrf_exempt

from . import sites_wrapper


@login_required
@csrf_exempt
def index(request):
    return render(request, 'abokistde/main.html')
