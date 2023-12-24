from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated

from abokistde.models import PublishingChannel


class PublishingChannelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PublishingChannel
        fields = ['id', 'name', 'url', 'description', 'thumbnail_url']


class PublishingChannelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PublishingChannel.objects.all()
    serializer_class = PublishingChannelSerializer
    filterset_fields = ['name']
    search_fields = ['name']


class PublishingChannelUserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PublishingChannelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PublishingChannel.objects.filter(
            usersubscription__user=self.request.user
        ).distinct().order_by("name")
