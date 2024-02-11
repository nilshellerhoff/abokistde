from django.db.models import Max
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated

from abokistde import sites_wrapper
from abokistde.models import UserSubscription, SubscriptionCategory


class SubscriptionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionCategory
        fields = ['id', 'name', 'icon']


class SubscriptionCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SubscriptionCategory.objects.filter(user=self.request.user)
