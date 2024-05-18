from rest_framework import viewsets, serializers, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from abokistde.models import PublishingChannel
from abokistde.sites_wrapper import getNewEpisodes
from api.views.provider import ProviderSerializer


class PublishingChannelSerializer(serializers.HyperlinkedModelSerializer):
    provider = ProviderSerializer()
    class Meta:
        model = PublishingChannel
        fields = ['id', 'name', 'url', 'description', 'thumbnail_url', 'provider']


class PublishingChannelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PublishingChannel.objects.all()
    serializer_class = PublishingChannelSerializer
    filterset_fields = ['name']
    search_fields = ['name', 'description']

    @action(detail=True, methods=['post'])
    def update_episodes(self, request, pk=None):
        channel: PublishingChannel = self.get_object()
        getNewEpisodes(channel_id=channel.id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PublishingChannelUserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PublishingChannelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PublishingChannel.objects.filter(
            usersubscription__user=self.request.user
        ).distinct().order_by("name")
