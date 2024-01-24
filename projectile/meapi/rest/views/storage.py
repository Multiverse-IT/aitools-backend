
from rest_framework import generics

from rest_framework.permissions import IsAuthenticatedOrReadOnly

from contentio.models import CommonStorage

from weapi.rest.serializers.storage import PrivateCommonStorageSerializer

class PublicCommonStorageList(generics.RetrieveAPIView):
    queryset = CommonStorage.objects.filter()
    serializer_class = PrivateCommonStorageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None

    def get_object(self):
        return CommonStorage.objects.first()
