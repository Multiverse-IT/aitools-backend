from rest_framework import generics

from catalogio.choices import ToolStatus
from catalogio.models import Tool

from ..serializers.tools import ToolListSerializer


class ToolList(generics.ListAPIView):
    queryset = Tool.objects.filter(status=ToolStatus.ACTIVE)
    serializer_class = ToolListSerializer

    def get_queryset(self):
        return self.queryset.filter(status=ToolStatus.ACTIVE)
