
from rest_framework import generics

from contentio.models import CommonStorage

from core.permissions import IsAdmin

from ..serializers.storage import PrivateCommonStorageSerializer

# class PrivateCommonStorageList(generics.ListCreateAPIView):
#     queryset = CommonStorage.objects.filter()
#     serializer_class = PrivateCommonStorageSerializer
#     permission_classes = [IsAdmin]


class PrivateCommonStorageDetail(generics.RetrieveUpdateAPIView):
    queryset = CommonStorage.objects.filter()
    serializer_class = PrivateCommonStorageSerializer
    permission_classes = [IsAdmin]
    pagination_class = None

    def get_object(self):
        return CommonStorage.objects.first()
