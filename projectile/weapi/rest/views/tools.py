
from rest_framework import generics
from catalogio.choices import ToolStatus
from catalogio.models import Tool

from ..serializers.tools import ToolListSerializer


class ToolList(generics.ListCreateAPIView):
    queryset = Tool.objects.filter(status=ToolStatus.ACTIVE)
    serializer_class = ToolListSerializer
    permission_classes = []

    def get_queryset(self):
        queryset = self.queryset

        search = self.request.query_params.get("search", None)
        category = self.request.query_params.get("category", None)

        if search is not None:
            queryset = queryset.filter(
                toolscategoryconnector__category__title__icontains=search
            )

        if category is not None:
            queryset = queryset.filter(toolscategoryconnector__category__title=category)

        return queryset


class ToolDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tool.objects.filter(status=ToolStatus.ACTIVE)
    serializer_class = ToolListSerializer
    permission_classes = []
    lookup_field = "slug"
