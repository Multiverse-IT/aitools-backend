from rest_framework import generics

from catalogio.models import Rating

from ..serializers.rating import RatingListDetaliSerializer


class RatingList(generics.ListCreateAPIView):
    queryset = Rating.objects.filter()
    serializer_class = RatingListDetaliSerializer
    permission_classes = []


class RatingDetail(generics.ListCreateAPIView):
    queryset = Rating.objects.filter()
    serializer_class = RatingListDetaliSerializer
    permission_classes = []
    lookup_field = "slug"
