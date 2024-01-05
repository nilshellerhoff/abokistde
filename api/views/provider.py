from rest_framework import serializers

from abokistde.models import Provider


class ProviderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Provider
        fields = ['id', 'name', 'url', 'icon_url']