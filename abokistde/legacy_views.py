from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.core.exceptions import ValidationError

from .models import Episode, PublishingChannel, UserSubscription, Provider
from django.contrib.auth.models import User
from django.contrib.auth import password_validation, authenticate, login, logout

from django.forms.models import model_to_dict
import json

from datetime import datetime, timedelta, timezone
import time
import uuid

from django.views.decorators.csrf import csrf_exempt

from . import sites_wrapper 

@csrf_exempt
def videos(request):

    print(request.user)
    print(request.user.id)

    # TODO get this to work
    # videos = Episode.objects.filter(publishing_channel__usersusbscription__in=UserSubscription.objects.filter(user=request.user)).order_by('-published')
    videos_ids = Episode.objects.raw("""
SELECT e.id FROM abokistde_episode e
INNER JOIN abokistde_publishingchannel c ON e.publishing_channel_id = c.id
INNER JOIN abokistde_usersubscription us ON c.id = us.publishing_channel_id
INNER JOIN auth_user u ON us.user_id = u.id
WHERE u.id = %s
    """ % request.user.id)

    videos = Episode.objects.filter(id__in=[v.id for v in videos_ids]).order_by('-published')
    videos_list = list(videos.values())

    for v1, v2 in zip(videos_list, videos):
        v1['rowid'] = v1['id']
        v1['channelName'] = v2.publishing_channel.name
        v1['channelThumbnail'] = v2.publishing_channel.thumbnail_url
        v1['channelid'] = v2.publishing_channel.channel_id
        v1['provider'] = v2.publishing_channel.provider.extractor.name
        v1['runtime'] = v2.duration
        v1['video_page_url'] = v2.thumbnail_url
        v1['timeSincePublished'] = int((datetime.now(timezone.utc) - v2.published).total_seconds())
        v1['thumbnail'] = v2.thumbnail_url

    channels_ids = PublishingChannel.objects.raw("""
SELECT c.id FROM abokistde_publishingchannel c
INNER JOIN abokistde_usersubscription us ON c.id = us.publishing_channel_id
INNER JOIN auth_user u ON us.user_id = u.id
WHERE u.id = %s
""" % request.user.id)
    channels = PublishingChannel.objects.filter(id__in=[c.id for c in channels_ids])
    channels_list = list(channels.values())

    for c1,c2 in zip(channels_list, channels):
        c1['rowid'] = c2.id
        c1['thumbnail'] = c2.thumbnail_url
        c1['video_page_url'] = c2.url
        
    # provider_favicons = { 'youtube': 'https://www.youtube.com/s/desktop/9528aa7e/img/favicon_32.png' }
    providers = Provider.objects.all()
    provider_names = [p.extractor.name for p in providers]
    provider_icons = [p.icon_url for p in providers]
    provider_favicons = { k: v for (k,v) in zip(provider_names, provider_icons)}
    results = {
        'videos': videos_list,
        'channels': channels_list,
        'providerFavicons': provider_favicons
    }
    return JsonResponse(results)

@csrf_exempt
def fetch_youtube(request):
    sites_wrapper.getNewEpisodes()
    return HttpResponseRedirect('/')

@csrf_exempt
def user_login(request):
    request_body = json.loads(request.body)
    username = request_body['username']
    password = request_body['password']

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        response = {
            "status": "success",
            "token": "1234"
        }
        return JsonResponse(response, status=200)
    else:
        response = {
            "status": "error",
            "message": "Wrong username or password"
        }
        return JsonResponse(response, status=400)

@csrf_exempt
def user_logout(request):
    logout(request)
    response = {
        "status": "success",
        "message": "Logged out"
    }
    return JsonResponse(response, status=200)

@csrf_exempt
def user_checktoken(request):
    # check if user is logged in
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "Not logged in"}, status=401)
    else:
        return JsonResponse({"status": "success", "message": "Logged in"}, status=200)

@csrf_exempt
def user_add(request):
    request_body = json.loads(request.body)
    username = request_body['username']
    password = request_body['password']

    # check if uername is taken
    if User.objects.filter(username=username).exists():
        response = {
            "status": "error",
            "message": "Username already taken"
        }
        return JsonResponse(response, status=400)
    
    # check if password is valid    
    try:
        # create user
        password_validation.validate_password(password)
        user = User.objects.create_user(username=username, password=password)
        response = {
            "status": "success",
            "message": "User created"
        }
        return JsonResponse(response, status=200)
    except ValidationError as e:
        response = {
            "status": "error",
            "message": e.messages[0]
        }
        return JsonResponse(response, status=400)

    except:
        response = {
            "status": "error",
            "message": "Something went wrong"
        }
        return JsonResponse(response, status=400)

@csrf_exempt
def search_online(request):
    searchterm = request.GET.get('query')
    channels_episodes = sites_wrapper.search(searchterm)

    channel_ids = [channel.id for channel in channels_episodes['channel']]
    channels = list(PublishingChannel.objects.filter(id__in=channel_ids).values())

    episode_ids = [episode.id for episode in channels_episodes['episode']]
    episodes = list(Episode.objects.filter(id__in=episode_ids).values())

    for r in channels:
        r['provider'] = {
            "id": 82,
            "name": "Youtube",
            "url": "https://www.youtube.com/",
            "icon_url": "https://www.youtube.com/s/desktop/5191a190/img/favicon_144x144.png"
        }

    return JsonResponse({
        "status": "success",
        "data": {
            "channels": channels,
            "episodes": episodes
        }
    })