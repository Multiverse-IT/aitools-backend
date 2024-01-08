
from rest_framework import generics

from contentio.models import CommonStorage

from weapi.rest.serializers.storage import PrivateCommonStorageSerializer

class PublicCommonStorageList(generics.ListAPIView):
    queryset = CommonStorage.objects.filter()
    serializer_class = PrivateCommonStorageSerializer
    permission_classes = []


class PublicCommonStorageDetail(generics.RetrieveAPIView):
    queryset = CommonStorage.objects.filter()
    serializer_class = PrivateCommonStorageSerializer
    permission_classes = []
    lookup_field = "uid"