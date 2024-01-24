from rest_framework import generics

from contentio.models import Redirect

from weapi.rest.serializers.redirect import PrivateRedirectSerializer


class PublicRedirectList(generics.ListAPIView):
    serializer_class = PrivateRedirectSerializer
    permission_classes = []

    def get_queryset(self):
        return Redirect.objects.filter()


class PublicRedirectDetail(generics.RetrieveAPIView):
    queryset = Redirect.objects.filter()
    serializer_class = PrivateRedirectSerializer
    permission_classes = []
    lookup_field = "uid"
