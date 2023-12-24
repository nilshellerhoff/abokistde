from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated

from abokistde.models import UserSubscription
from api.views.publishing_channel import PublishingChannelSerializer


class UserSubscriptionSerializer(serializers.ModelSerializer):
    # publishing_channel = PublishingChannelSerializer(many=False)
    class Meta:
        model = UserSubscription
        fields = ['id', 'publishing_channel']


class UserSubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = UserSubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserSubscription.objects.filter(
            user=self.request.user
        )
