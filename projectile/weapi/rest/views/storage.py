
from rest_framework import generics

from contentio.models import CommonStorage

from core.permissions import IsAdmin

from ..serializers.storage import PrivateCommonStorageSerializer

class PrivateCommonStorageList(generics.ListAPIView):
    queryset = CommonStorage.objects.filter()
    serializer_class = PrivateCommonStorageSerializer
    permission_classes = [IsAdmin]


class PrivateCommonStorageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CommonStorage.objects.filter()
    serializer_class = PrivateCommonStorageSerializer
    permission_classes = [IsAdmin]
    lookup_field = "uid"