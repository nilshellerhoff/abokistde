from django.db.models import Max
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated

from abokistde import sites_wrapper
from abokistde.models import UserSubscription
from api.views.publishing_channel import PublishingChannelSerializer
from api.views.subscription_category import SubscriptionCategorySerializer


class UserSubscriptionSerializer(serializers.ModelSerializer):
    publishing_channel = PublishingChannelSerializer(many=False, read_only=True)
    category = SubscriptionCategorySerializer(many=False, read_only=True)

    class Meta:
        model = UserSubscription
        fields = ['id', 'publishing_channel', 'publishing_channel_id', 'category', 'category_id']
        extra_kwargs = {
            'publishing_channel_id': {'source': 'publishing_channel'},
            'category_id': {'source': 'category'}
        }


class UserSubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = UserSubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserSubscription.objects.filter(
            user=self.request.user
        ).annotate(last_publish=Max("publishing_channel__episode__published")).order_by("-last_publish")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        publishing_channel = serializer.validated_data['publishing_channel']
        sites_wrapper.getNewEpisodes(channel_id=publishing_channel.id)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if instance.user == self.request.user:
            instance.delete()
