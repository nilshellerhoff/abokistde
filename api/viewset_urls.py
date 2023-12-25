from django.urls import include, path
from rest_framework import routers

from api.views.episode import EpisodeViewSet, EpisodeUserViewSet
from api.views.publishing_channel import PublishingChannelViewSet, PublishingChannelUserViewSet
from api.views.user_subscription import UserSubscriptionViewSet

router = routers.DefaultRouter()
router.register(r'episode', EpisodeViewSet)
router.register(r'episode_user', EpisodeUserViewSet, basename='episode_user')
router.register(r'publishing_channel', PublishingChannelViewSet)
router.register(r'publishing_channel_user', PublishingChannelUserViewSet, basename='publishing_channel_user')
router.register(r'user_subscription', UserSubscriptionViewSet, basename='user_subscription')

urlpatterns = [
    path('', include(router.urls)),
]
