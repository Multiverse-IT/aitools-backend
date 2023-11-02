from catalogio.choices import ToolStatus
from catalogio.models import Tool
from rest_framework import generics

from ..serializers.tools import ToolListSerializer, ToolRequestDetalSerializer


class ToolList(generics.ListCreateAPIView):
    queryset = Tool.objects.get_status_editable()
    serializer_class = ToolListSerializer
    permission_classes = []

    def get_queryset(self):
        queryset = self.queryset

        search = self.request.query_params.get("search", None)
        subcategory = self.request.query_params.get("subcategory", [])
        requested = self.request.query_params.get("requested", None)

        if search is not None:
            queryset = queryset.filter(
                toolscategoryconnector__subcategory__title__icontains=search
            )

        if subcategory:
            subcategories = subcategory.split(",")
            queryset = queryset.filter(
                toolscategoryconnector__subcategory__slug__in=subcategories
            )

        if requested:
            queryset = queryset.filter(requested=requested)

        return queryset.distinct()


class ToolDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tool.objects.get_status_editable()
    serializer_class = ToolListSerializer
    permission_classes = []
    lookup_field = "slug"


class RequestToolResponseDetail(generics.RetrieveUpdateAPIView):
    queryset = Tool.objects.get_status_requested()
    serializer_class = ToolRequestDetalSerializer
    permission_classes = []
    lookup_field = "slug"