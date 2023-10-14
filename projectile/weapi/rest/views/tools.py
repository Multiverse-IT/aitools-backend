from rest_framework import generics

from catalogio.choices import ToolStatus
from catalogio.models import Tool

from ..serializers.tools import ToolListSerializer


class ToolList(generics.ListCreateAPIView):
    queryset = Tool.objects.filter(status=ToolStatus.ACTIVE)
    serializer_class = ToolListSerializer

    def get_queryset(self):
        search = self.request.query_params.get("search", None)
        if search:
            return self.queryset.filter(name__icontains=search)
        return self.queryset.filter(status=ToolStatus.ACTIVE)


class ToolDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tool.objects.filter(status=ToolStatus.ACTIVE)
    serializer_class = ToolListSerializer
    lookup_field = "slug"