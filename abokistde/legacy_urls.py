from django.urls import path
from . import legacy_views as views

urlpatterns = [
    # Legacy endpoints for old frontend
    path('api/videos', views.videos, name="videos"),
    path('fetch_youtube', views.fetch_youtube, name='fetch_youtube'),
    path('user/login', views.user_login, name='user_login'),
    path('user/logout', views.user_logout, name='user_logout'),
    path('user/check_token', views.user_checktoken, name='user_checktoken'),
    path('user/add', views.user_add, name='user_add'),
    path('api/insert_channel', views.insert_channel, name='insert_channel'),
    path('api/delete_channel', views.delete_channel, name='delete_channel'),
]