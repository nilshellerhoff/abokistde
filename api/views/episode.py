from django_filters import BooleanFilter, filterset
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets, serializers, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from abokistde.models import Episode
from api.views.publishing_channel import PublishingChannelSerializer


class EpisodeSerializer(serializers.ModelSerializer):
    publishing_channel = PublishingChannelSerializer(many=False)
    is_hidden = serializers.SerializerMethodField(read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Episode
        fields = ['id', 'title', 'description', 'thumbnail_url', 'url', 'published',  'is_hidden', 'is_subscribed', 'publishing_channel']

    def get_is_hidden(self, obj):
        return self.context['request'].user.hiddenepisode_set.filter(episode=obj).exists()

    def get_is_subscribed(self, obj):
        return self.context['request'].user.usersubscription_set.filter(publishing_channel=obj.publishing_channel).exists()


class EpisodeFilter(FilterSet):
    is_hidden = BooleanFilter(method='filter_is_hidden')
    is_subscribed = BooleanFilter(method='filter_is_subscribed')
    publishing_channel_id = filterset.NumberFilter(field_name='publishing_channel__id')

    def filter_is_hidden(self, queryset, name, value):
        if value is not None:
            if value:
                queryset = queryset.filter(hiddenepisode__user=self.request.user)
            else:
                queryset = queryset.exclude(hiddenepisode__user=self.request.user)

        return queryset

    def filter_is_subscribed(self, queryset, name, value):
        if value is not None:
            if value:
                queryset = queryset.filter(publishing_channel__usersubscription__user=self.request.user)
            else:
                queryset = queryset.exclude(publishing_channel__usersubscription__user=self.request.user)

        return queryset


class EpisodeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EpisodeSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = EpisodeFilter

    def get_queryset(self):
        return Episode.objects.order_by(
            "-published").distinct()

    @action(detail=True, methods=['post'])
    def hide(self, request, pk=None):
        episode = self.get_object()
        user = request.user
        if not user.hiddenepisode_set.filter(episode=episode).exists():
            user.hiddenepisode_set.create(episode=episode)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def unhide(self, request, pk=None):
        episode = self.get_object()
        user = request.user
        if user.hiddenepisode_set.filter(episode=episode).exists():
            user.hiddenepisode_set.filter(episode=episode).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
