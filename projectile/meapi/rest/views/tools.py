from datetime import datetime

from rest_framework import generics, permissions
from django.db.models import Q, F

from catalogio.choices import ToolStatus
from catalogio.models import SavedTool, Tool
from catalogio.permissions import IsAuthenticatedOrReadOnlyForUserTool
from search.models import Keyword, KeywordSearch
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
            # Split the search string by comma, filter out words with less than 2 characters
            search_words = [word.strip() for word in search.split(',') if len(word.strip()) >= 2]

            # Build a single Q object for all search conditions
            q_object = Q()
            for word in search_words:
                q_object |= (
                    Q(name__icontains=word) |
                    Q(description__icontains=word) |
                    Q(toolscategoryconnector__subcategory__title__icontains=word) |
                    Q(toolscategoryconnector__category__title__icontains=word)
                )

            # Filter tools based on the search words in multiple fields
            if search_words:
                queryset = queryset.filter(q_object)

                # Save the search keyword and associate it with the user if authenticated
                user = self.request.user
                keyword, created = Keyword.objects.get_or_create(name=search)
                if user.is_authenticated:
                    keyword_search, created = KeywordSearch.objects.get_or_create(keyword=keyword, user=user)
                    if not created:
                        keyword_search.search_count = F('search_count') + 1
                        keyword_search.save()
                else:
                    keyword_search, created = KeywordSearch.objects.get_or_create(keyword=keyword)
                    if not created:
                        keyword_search.search_count = F('search_count') + 1
                        keyword_search.save()

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
