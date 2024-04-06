from django.db.models import Q

from rest_framework import generics

from catalogio.choices import ToolStatus, VerifiedStatus
from catalogio.models import Tool, TopHundredTools

from core.permissions import IsAdmin

from ..serializers.tools import (
    ToolListSerializer,
    ToolRequestDetailSerializer,
    ToolWithVerifiedStatus,
    PrivateTopHundredToolsSerializer
)


class ToolList(generics.ListCreateAPIView):
    queryset = Tool.objects.get_status_editable()
    serializer_class = ToolListSerializer
    permission_classes = []

    def get_queryset(self):
        queryset = self.queryset.exclude(requested=True, status=ToolStatus.PENDING)
        search = self.request.query_params.get("search", None)
        subcategory = self.request.query_params.get("subcategory", [])
        requested = self.request.query_params.get("requested", None)
        features = self.request.query_params.get("features", [])
        trending = self.request.query_params.get("trending", None)

        if search is not None:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(description__icontains=search)
                | Q(toolscategoryconnector__subcategory__title__icontains=search)
                | Q(toolscategoryconnector__category__title__icontains=search)
            )

        if subcategory:
            subcategories = subcategory.split(",")
            queryset = queryset.filter(
                toolscategoryconnector__subcategory__slug__in=subcategories
            )

        if requested:
            queryset = Tool.objects.filter(
                requested=requested, status=ToolStatus.PENDING
            )

        if trending:
            queryset = queryset.filter(is_trending=trending)

        if features:
            features = features.split(",")
            queryset = queryset.filter(toolsconnector__feature__slug__in=features)

        return queryset.distinct()


class ToolDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tool.objects.get_status_editable()
    serializer_class = ToolListSerializer
    permission_classes = []
    lookup_field = "slug"


class RequestToolResponseDetail(generics.RetrieveUpdateAPIView):
    queryset = Tool.objects.get_status_requested()
    serializer_class = ToolRequestDetailSerializer
    permission_classes = []
    lookup_field = "slug"


class PrivateCodeVerifyList(generics.ListAPIView):
    queryset = Tool.objects.get_status_active()
    serializer_class = ToolListSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        queryset = self.queryset.filter(verified_status=VerifiedStatus.PENDING)
        return queryset


class PrivateCodeVerifyDetail(generics.RetrieveUpdateAPIView):
    queryset = Tool.objects.get_status_active()
    serializer_class = ToolWithVerifiedStatus
    permission_classes = [IsAdmin]

    def get_object(self):
        slug = self.kwargs.get("slug", None)
        return generics.get_object_or_404(
            self.queryset.filter(), verified_status=VerifiedStatus.PENDING, slug=slug
        )


class PrivateTopHundredToolsList(generics.ListCreateAPIView):
    queryset = TopHundredTools.objects.select_related("feature_tool").filter().order_by("-is_add", "-created_at")
    serializer_class = PrivateTopHundredToolsSerializer
    permission_classes = [IsAdmin]

class PrivateTopHundredToolsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TopHundredTools.objects.select_related("feature_tool").filter().order_by("-is_add", "-created_at")
    serializer_class = PrivateTopHundredToolsSerializer
    permission_classes = [IsAdmin]
    lookup_field = "slug"
