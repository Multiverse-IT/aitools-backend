from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.db.models import Avg, Count, F, Q
from django.utils import timezone

from catalogio.choices import ToolStatus
from catalogio.models import SavedTool, Tool

from rest_framework import generics
from search.models import Keyword, KeywordSearch

from ..permissions import CustomIdentityHeaderPermission
from ..serializers.tools import (
    PublicTooDetailSerializer,
    PublicToolListSerializer,
    PublicTrendingToolListSerializer,
)

User = get_user_model()


class PublicToolList(generics.ListCreateAPIView):
    queryset = Tool.objects.filter(status=ToolStatus.ACTIVE)
    serializer_class = PublicToolListSerializer
    permission_classes = [CustomIdentityHeaderPermission]

    def get_queryset(self):
        queryset = self.queryset

        search = self.request.query_params.get("search", None)
        subcategory = self.request.query_params.get("subcategory", [])
        features = self.request.query_params.get("features", [])
        ordering_param = self.request.query_params.get("ordering", None)
        time_range = self.request.query_params.get("time_range", None)

        if search is not None:
            search_words = [
                word.strip() for word in search.split(",") if len(word.strip()) >= 2
            ]

            q_object = Q()
            for word in search_words:
                q_object |= (
                    Q(name__icontains=word)
                    | Q(description__icontains=word)
                    | Q(toolscategoryconnector__subcategory__title__icontains=word)
                    | Q(toolscategoryconnector__category__title__icontains=word)
                )

            # Filter tools based on the search words in multiple fields
            if search_words:
                queryset = queryset.filter(q_object)

                # Save the search keyword and associate it with the user if authenticated
                user = self.request.user
                keyword, created = Keyword.objects.get_or_create(name=search)
            
                if user.is_authenticated:
                    keyword_search = KeywordSearch.objects.filter(keyword=keyword).first()
                    
                    if not keyword_search:
                        keyword_search = KeywordSearch.objects.create(keyword=keyword, user=user)
                    keyword_search.search_count += 1
                    keyword_search.save()

                else:
                    keyword_search = KeywordSearch.objects.filter(keyword=keyword).first()
                    if not keyword_search:
                        keyword_search = KeywordSearch.objects.create(keyword=keyword)
                    keyword_search.search_count += 1
                    keyword_search.save()

        if time_range:
            now = timezone.now()

            if time_range == "this_week":
                start_date = now - timedelta(days=now.weekday())
                queryset = queryset.filter(created_at__gte=start_date)

            elif time_range == "this_month":
                start_date = now.replace(day=1)
                queryset = queryset.filter(created_at__gte=start_date)

            elif time_range == "last_month":
                last_month_end = now.replace(day=1) - timedelta(days=1)
                last_month_start = last_month_end.replace(day=1)
                queryset = queryset.filter(
                    created_at__range=(last_month_start, last_month_end)
                )

        if subcategory:
            subcategories = subcategory.split(",")
            queryset = queryset.filter(
                toolscategoryconnector__subcategory__slug__in=subcategories
            )

        if features:
            features = features.split(",")
            queryset = queryset.filter(toolsconnector__feature__slug__in=features)

        if ordering_param:
            if ordering_param == "most_loved":
                queryset = queryset.order_by("-save_count")
            elif ordering_param == "average_ratings":
                queryset.annotate(average_ratings=Avg("toolsconnector__rating__rating")).order_by("-average_ratings")

            elif ordering_param == "created_at":
                queryset = queryset.order_by("-created_at")

        queryset = queryset.annotate(
            average_ratings=Avg("toolsconnector__rating__rating")
        )
        return queryset.distinct()

class PublicToolDetail(generics.RetrieveUpdateAPIView):
    queryset = Tool.objects.filter(status=ToolStatus.ACTIVE)
    serializer_class = PublicTooDetailSerializer
    permission_classes = [CustomIdentityHeaderPermission]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            average_ratings=Avg("toolsconnector__rating__rating")
        )

        return queryset.distinct()


class UserLoveToolList(generics.ListAPIView):
    permission_classes = [CustomIdentityHeaderPermission]
    serializer_class = PublicTooDetailSerializer

    def get_queryset(self):
        identity = self.request.headers.get("identity")
        user = User.objects.filter(id=identity).first()

        if not user:
            return Tool.objects.none()

        # user = self.request.user
        save_tool_ids = SavedTool.objects.filter(user=user).values_list(
            "save_tool_id", flat=True
        )
        return Tool.objects.filter(id__in=save_tool_ids)


class PublicToolTodayList(generics.ListAPIView):
    serializer_class = PublicToolListSerializer

    def get_queryset(self):
        today = datetime.now().date()
        return Tool.objects.filter(created_at__date=today, status=ToolStatus.ACTIVE)


class PublicTrendingToolList(generics.ListAPIView):
    queryset = Tool.objects.filter(status=ToolStatus.ACTIVE)
    serializer_class = PublicTrendingToolListSerializer
    permission_classes = [CustomIdentityHeaderPermission]

    def get_queryset(self):
        queryset = self.queryset
        time_range = self.request.query_params.get("time_range", None)

        if time_range:
            now = timezone.now()

            if time_range == "this_week":
                start_date = now - timedelta(days=now.weekday())
                queryset = queryset.annotate(
                    total_saved_tools=Count(
                        "save_tool", filter=Q(save_tool__created_at__gte=start_date)
                    )
                ).filter(total_saved_tools__gt=3).order_by("-total_saved_tools")

            elif time_range == "this_month":
                start_date = now.replace(day=1)
                queryset = queryset.annotate(
                    total_saved_tools=Count(
                        "save_tool", filter=Q(save_tool__created_at__gte=start_date)
                    )
                ).filter(total_saved_tools__gt=3).order_by("-total_saved_tools")

            elif time_range == "last_month":
                last_month_end = now.replace(day=1) - timedelta(days=1)
                last_month_start = last_month_end.replace(day=1)
                queryset = queryset.annotate(
                    total_saved_tools=Count(
                        "save_tool",
                        filter=Q(
                            save_tool__created_at__range=(
                                last_month_start,
                                last_month_end,
                            )
                        ),
                    )
                ).filter(total_saved_tools__gt=3).order_by("-total_saved_tools")

        return queryset


class PublicTrendingToolDetail(generics.RetrieveAPIView):
    queryset = Tool.objects.filter(status=ToolStatus.ACTIVE)
    serializer_class = PublicTrendingToolListSerializer
    permission_classes = [CustomIdentityHeaderPermission]
    lookup_field = "slug"
