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
    episode_values = [
        "title",
        "url",
        "thumbnail_url",
        "publishing_channel__name",
        "publishing_channel__id",
        "publishing_channel__thumbnail_url",
    ]

    episodes = Episode.objects.filter(publishing_channel__usersubscription__user=request.user).order_by(
        "-published").distinct().values(*episode_values)[:1000]
    channels = PublishingChannel.objects.filter(
        usersubscription__user=request.user
    ).distinct().order_by("name").values()

    context = {
        "channels": channels,
        "episodes": episodes,
    }

    return render(request, 'abokistde/main.html', context)
