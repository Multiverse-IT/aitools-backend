from rest_framework import generics
from catalogio.models import FeatureTool
from weapi.rest.serializers.feature_tool import PrivateFeatureToolSerializer

class PublicFeatureToolList(generics.ListAPIView):
    queryset = FeatureTool.objects.filter()
    serializer_class = PrivateFeatureToolSerializer
    permission_classes = []


class PublicFeatureToolDetail(generics.RetrieveAPIView):
    queryset = FeatureTool.objects.filter()
    serializer_class = PrivateFeatureToolSerializer
    lookup_field = "slug"
    permission_classes = []