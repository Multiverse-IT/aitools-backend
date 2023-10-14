from rest_framework import generics

from catalogio.models import Feature

from ..serializers.feature import FeatureListDetailSerializer


class FeatureList(generics.ListCreateAPIView):
    serializer_class = FeatureListDetailSerializer

    def get_queryset(self):
        return Feature.objects.filter()


class FeatureDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feature.objects.filter()
    serializer_class = FeatureListDetailSerializer
    lookup_field = "slug"
