
from catalogio.choices import ToolStatus
from catalogio.models import Tool
from rest_framework import generics

from ..serializers.tools import PublicTooDetailSerializer, PublicToolListSerializer


class PublicToolList(generics.ListAPIView):
    queryset = Tool.objects.filter(status=ToolStatus.ACTIVE)
    serializer_class = PublicToolListSerializer
    permission_classes = []

    def get_queryset(self):
        queryset = self.queryset

        search = self.request.query_params.get("search", None)
        subcategory = self.request.query_params.get("subcategory", [])

        if search is not None:
            queryset = queryset.filter(
                toolscategoryconnector__subcategory__title__icontains=search
            )

        if subcategory:
            subcategories = subcategory.split(",")
            queryset = queryset.filter(
                toolscategoryconnector__subcategory__slug__in=subcategories
            )

        return queryset.distinct()

from rest_framework import permissions

class PublicToolDetail(generics.RetrieveUpdateAPIView):
    queryset = Tool.objects.filter(status=ToolStatus.ACTIVE)
    serializer_class = PublicTooDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "slug"