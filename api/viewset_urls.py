from django.urls import include, path
from rest_framework import routers

from api.views.episode import EpisodeViewSet
from api.views.publishing_channel import PublishingChannelViewSet, PublishingChannelUserViewSet
from api.views.subscription_category import SubscriptionCategoryViewSet
from api.views.user_subscription import UserSubscriptionViewSet

router = routers.DefaultRouter()
router.register(r'episode', EpisodeViewSet, basename="episode")
router.register(r'episode_user', EpisodeViewSet, basename='episode_user')
router.register(r'publishing_channel', PublishingChannelViewSet, basename='publishing_channel')
router.register(r'publishing_channel_user', PublishingChannelUserViewSet, basename='publishing_channel_user')
router.register(r'subscription_category', SubscriptionCategoryViewSet, basename='subscription_category')
router.register(r'user_subscription', UserSubscriptionViewSet, basename='user_subscription')

urlpatterns = [
    path('', include(router.urls)),
]
