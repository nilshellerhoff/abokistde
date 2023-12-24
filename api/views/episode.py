from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated

from abokistde.models import Episode
from api.views.publishing_channel import PublishingChannelSerializer


class EpisodeSerializer(serializers.ModelSerializer):
    publishing_channel = PublishingChannelSerializer(many=False)

    class Meta:
        model = Episode
        fields = ['id', 'title', 'description', 'thumbnail_url', 'url', 'publishing_channel']


class EpisodeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer
    filterset_fields = ['publishing_channel']


class EpisodeUserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EpisodeSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['publishing_channel']

    def get_queryset(self):
        return Episode.objects.filter(publishing_channel__usersubscription__user=self.request.user).order_by(
            "-published").distinct()
