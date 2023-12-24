from django.urls import path
from abokistde.legacy_views import videos, fetch_youtube, user_login, user_logout, user_checktoken, user_add, \
    insert_channel, insert_channel_by_id, delete_channel, search_online

urlpatterns = [
    # Legacy endpoints for old frontend
    path('api/videos', videos, name="videos"),
    path('fetch_youtube', fetch_youtube, name='fetch_youtube'),
    path('user/login', user_login, name='user_login'),
    path('user/logout', user_logout, name='user_logout'),
    path('user/check_token', user_checktoken, name='user_checktoken'),
    path('user/add', user_add, name='user_add'),
    path('api/insert_channel', insert_channel, name='insert_channel'),
    path('api/insert_channel_by_id', insert_channel_by_id, name='insert_channel_by_id'),
    path('api/delete_channel', delete_channel, name='delete_channel'),
    path('search_online', search_online, name='search_online'),
]
