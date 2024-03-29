from rest_framework import generics

from contentio.models import Redirect

from ..serializers.redirect import PrivateRedirectSerializer
from core.permissions import IsAdmin


class PrivateRedirectList(generics.ListCreateAPIView):
    serializer_class = PrivateRedirectSerializer
    permission_classes = [IsAdmin]
    pagination_class = None

    def get_queryset(self):
        return Redirect.objects.filter()


class PrivateRedirectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Redirect.objects.filter()
    serializer_class = PrivateRedirectSerializer
    permission_classes = [IsAdmin]
    pagination_class = None
    lookup_field = "uid"
