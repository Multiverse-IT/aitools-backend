from django.contrib.auth import get_user_model

from rest_framework import generics

from catalogio.models import Rating
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..permissions import CustomIdentityHeaderPermission
from ..serializers.ratings import MeRatingListDetaliSerializer
from rest_framework.pagination import PageNumberPagination
class CustomPaginationFor3Item(PageNumberPagination):
    page_size = 3

User = get_user_model()

class RatingList(generics.ListCreateAPIView):
    queryset = Rating.objects.filter()
    serializer_class = MeRatingListDetaliSerializer
    permission_classes = [CustomIdentityHeaderPermission]

    def get_queryset(self):
        identity = self.request.headers.get("identity")
        user = User.objects.filter(id=identity).first()

        if not user:
            return Rating.objects.none()

        return self.queryset.filter(user=user)

class RatingDetail(generics.RetrieveAPIView):
    queryset = Rating.objects.filter()
    serializer_class = MeRatingListDetaliSerializer
    permission_classes = [CustomIdentityHeaderPermission]
    lookup_field = "uid"

    def get_queryset(self):
        identity = self.request.headers.get("identity")
        user = User.objects.filter(id=identity).first()
        if not user:
            return Rating.objects.none()
        return Rating.objects.filter(user=user)



class SingleToolRatingDetail(generics.ListAPIView):
    queryset = Rating.objects.filter()
    serializer_class = MeRatingListDetaliSerializer
    pagination_class = CustomPaginationFor3Item


    def get_queryset(self):
        slug = self.kwargs.get("tool_slug", None)
        return Rating.objects.filter(toolsconnector__tool__slug=slug)