from datetime import datetime

from rest_framework import generics, permissions

from catalogio.choices import ToolStatus
from catalogio.models import SavedTool, Tool
from catalogio.permissions import IsAuthenticatedOrReadOnlyForUserTool

from ..serializers.tools import PublicTooDetailSerializer, PublicToolListSerializer


class PublicToolList(generics.ListCreateAPIView):
    queryset = Tool.objects.filter(status=ToolStatus.ACTIVE)
    serializer_class = PublicToolListSerializer
    permission_classes = [IsAuthenticatedOrReadOnlyForUserTool]

    def get_queryset(self):
        queryset = self.queryset

        search = self.request.query_params.get("search", None)
        subcategory = self.request.query_params.get("subcategory", [])
        features = self.request.query_params.get("features", [])
        # pricing = self.request.query_params.get("pricing")

        if search is not None:
            queryset = queryset.filter(
                toolscategoryconnector__subcategory__title__icontains=search
            )

        if subcategory:
            subcategories = subcategory.split(",")
            queryset = queryset.filter(
                toolscategoryconnector__subcategory__slug__in=subcategories
            )

        if features:
            features = features.split(",")
            queryset = queryset.filter(toolsconnector__feature__slug__in=features)

        return queryset.distinct()


class PublicToolDetail(generics.RetrieveUpdateAPIView):
    queryset = Tool.objects.filter(status=ToolStatus.ACTIVE)
    serializer_class = PublicTooDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "slug"


class UserLoveToolList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PublicTooDetailSerializer

    def get_queryset(self):
        user = self.request.user
        save_tool_ids = SavedTool.objects.filter(user=user).values_list(
            "save_tool_id", flat=True
        )
        return Tool.objects.filter(id__in=save_tool_ids)


class PublicToolTodayList(generics.ListAPIView):
    serializer_class = PublicToolListSerializer

    def get_queryset(self):
        today = datetime.now().date()
        return Tool.objects.filter(created_at__date=today, status=ToolStatus.ACTIVE)
