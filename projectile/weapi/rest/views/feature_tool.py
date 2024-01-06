from rest_framework import generics
from catalogio.models import FeatureTool
from core.permissions import IsAdmin

from ..serializers.feature_tool import PrivateFeatureToolSerializer, PrivateFeatureToolDetailSerializer


class PrivateFeatureToolList(generics.ListCreateAPIView):
    queryset = FeatureTool.objects.filter()
    serializer_class = PrivateFeatureToolSerializer
    permission_classes = [IsAdmin]


class PrivateFeatureToolDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FeatureTool.objects.filter()
    serializer_class = PrivateFeatureToolDetailSerializer
    lookup_field = "slug"
    permission_classes = [IsAdmin]
