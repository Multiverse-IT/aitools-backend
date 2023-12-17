from catalogio.models import Tool
from rest_framework import generics

from ..serializers.tools import PublicApiToolListSerializer


class PublicApiToolList(generics.ListAPIView):
    queryset = Tool.objects.get_status_active()
    serializer_class = PublicApiToolListSerializer
    permission_classes = []
    pagination_class = None
