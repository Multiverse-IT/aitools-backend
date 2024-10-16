from datetime import datetime, timedelta

from catalogio.choices import ToolStatus
from catalogio.models import Tool, Deal
from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import generics
from search.models import KeywordSearch

from ..serializers.count import PublicCountSerializer, PublicSubcategoryCountSerializer


class CountOfEveryThingList(generics.RetrieveAPIView):
    serializer_class = PublicCountSerializer

    def get_object(self):
        today = datetime.now().date()
        today = datetime.now().date()
        now = timezone.now()
        start_date = now  - timedelta(days=now.weekday())

        queryset = Tool.objects.filter(status=ToolStatus.ACTIVE)
        today_search_count = KeywordSearch.objects.filter(
            created_at__date=timezone.now().date()
        ).count()
        deals_count = Deal.objects.filter()

        trending_tools_count = (
                    queryset.annotate(
                        total_saved_tools=Count(
                            "save_tool", filter=Q(save_tool__created_at__gte=start_date)
                        )
                    )
                    .filter(total_saved_tools__gt=3)
                    .order_by("-total_saved_tools")
                ).count()

        return {
            "today_search_count": today_search_count,
            "total_tools": queryset.aggregate(total_tools=Count("id"))["total_tools"],
            "today_created_tools": queryset.aggregate(
                today_created_tools=Count("id", filter=Q(created_at__date=today))
            )["today_created_tools"],
            "trending_tools": trending_tools_count,
            "total_deals": deals_count.count()
        }


class PublicSubcategoryToolsCountList(generics.RetrieveAPIView):
    serializer_class = PublicSubcategoryCountSerializer

    def get_object(self):
        slug = self.kwargs.get("subcategory_slug", None)
        today = datetime.now().date()
        now = timezone.now()
        start_date = now - timedelta(days=now.weekday())

        queryset = Tool.objects.filter(
            toolscategoryconnector__subcategory__slug=slug, status=ToolStatus.ACTIVE).distinct().exclude(is_new=False)

        trending_tools_count = (
                    queryset.annotate(
                        total_saved_tools=Count(
                            "save_tool", filter=Q(save_tool__created_at__gte=start_date)
                        )
                    )
                    .filter(total_saved_tools__gt=3)
                    .order_by("-total_saved_tools")
                ).count()
        
        return {
            "total_tools": queryset.aggregate(total_tools=Count("id"))["total_tools"],
            "today_created_tools": queryset.aggregate(
                today_created_tools=Count("id", filter=Q(created_at__date=today))
            )["today_created_tools"],
            "trending_tools": trending_tools_count
        }