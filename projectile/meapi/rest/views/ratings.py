from django.contrib.auth import get_user_model

from rest_framework import generics

from catalogio.models import Rating
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..permissions import CustomIdentityHeaderPermission
from ..serializers.ratings import MeRatingListDetaliSerializer

User = get_user_model()

class RatingList(generics.ListCreateAPIView):
    queryset = Rating.objects.filter()
    serializer_class = MeRatingListDetaliSerializer
    permission_classes = [CustomIdentityHeaderPermission]

    def get_queryset(self):
        user = self.request.user
        identity = self.request.headers.get("identity")
        user = User.objects.filter(id=identity).first()

        if not user:
            return Rating.objects.none()

        return self.queryset.filter(user=user)

class RatingDetail(generics.RetrieveUpdateAPIView):
    queryset = Rating.objects.filter()
    serializer_class = MeRatingListDetaliSerializer
    permission_classes = [CustomIdentityHeaderPermission]
    lookup_field = "slug"

    def get_queryset(self):
        identity = self.request.headers.get("identity")
        user = User.objects.filter(id=identity).first()
        if not user:
            return Rating.objects.none()
        return Rating.objects.filter(user=user)