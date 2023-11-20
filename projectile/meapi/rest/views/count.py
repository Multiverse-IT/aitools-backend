from datetime import datetime

from django.db.models import Count, Q
from django.utils import timezone

from rest_framework import generics

from catalogio.choices import ToolStatus
from catalogio.models import Tool

from search.models import KeywordSearch

from ..serializers.count import PublicCountSerializer

class CountOfEveryThingList(generics.RetrieveAPIView):
    serializer_class = PublicCountSerializer

    def get_object(self):
        today = datetime.now().date()

        queryset = Tool.objects.filter(status=ToolStatus.ACTIVE).annotate(
            total_tools=Count('id'),
            today_created_tools=Count('id', filter=Q(created_at__date=today)),
            trending_tools=Count('id', filter=Q(is_trending=True)),
            love_tools_count=Count('love_tool', distinct=True),  # Use the related name 'love_tool'
        )
        today_search_count = KeywordSearch.objects.filter(created_at__date=timezone.now().date()).count()

        return {
            "today_search_count": today_search_count,
            "total_tools": queryset.aggregate(total_tools=Count('id'))['total_tools'],
            "today_created_tools": queryset.aggregate(today_created_tools=Count('id', filter=Q(created_at__date=today)))['today_created_tools'],
            "trending_tools": queryset.aggregate(trending_tools=Count('id', filter=Q(is_trending=True)))['trending_tools'],
        }
