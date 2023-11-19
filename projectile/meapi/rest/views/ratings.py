from rest_framework import generics

from catalogio.models import Rating

from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..serializers.ratings import MeRatingListDetaliSerializer

class RatingList(generics.ListCreateAPIView):
    queryset = Rating.objects.filter()
    serializer_class = MeRatingListDetaliSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)

class RatingDetail(generics.RetrieveUpdateAPIView):
    queryset = Rating.objects.filter()
    serializer_class = MeRatingListDetaliSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "slug"