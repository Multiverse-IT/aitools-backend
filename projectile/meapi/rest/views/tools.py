from datetime import date, datetime, timedelta

from django.contrib.auth import get_user_model
from django.db.models import Prefetch, Q, Avg, Count, Case, When, Value, IntegerField, BooleanField

from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from catalogio.choices import ToolStatus, PricingKind, VerifiedStatus
from catalogio.models import (
    SavedTool,
    Tool,
    SubCategory,
    TopHundredTools,
    BestAlternativeTool,
    ToolsCategoryConnector,
    ToolsConnector,
    FeatureTool,
)

from common.utils import CustomPagination10

from meapi.rest.scrape.link_find import check_code_presence

from search.models import Keyword, KeywordSearch

from ..permissions import CustomIdentityHeaderPermission
from ..serializers.tools import (
    PublicSubCategoryToolSerializer,
    PublicTooDetailSerializer,
    PublicToolListSerializer,
    PublicTrendingToolListSerializer,
)
from weapi.rest.serializers.tools import PrivateTopHundredToolsSerializer
from weapi.rest.serializers.feature_tool import PrivateBestAlternativeToolSerializer

User = get_user_model()

class PublicRandomSearch(generics.ListAPIView):
    queryset = Tool.objects.filter(status=ToolStatus.ACTIVE)
    serializer_class = PublicToolListSerializer

    def get_queryset(self):
        queryset = self.queryset.order_by("-created_at")
        search = self.request.query_params.get("search", None)

        if search is not None:
            search_words = [
                word.strip() for word in search.split(" ") if len(word.strip()) >= 2
            ]

            q_object = Q()
            for word in search_words:
                q_object |= (
                    Q(name__icontains=word)
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
                    keyword_search = KeywordSearch.objects.filter(
                        keyword=keyword
                    ).first()

                    if not keyword_search:
                        keyword_search = KeywordSearch.objects.create(
                            keyword=keyword, user=user
                        )
                    keyword_search.search_count += 1
                    keyword_search.save()

                else:
                    keyword_search = KeywordSearch.objects.filter(
                        keyword=keyword
                    ).first()
                    if not keyword_search:
                        keyword_search = KeywordSearch.objects.create(keyword=keyword)
                    keyword_search.search_count += 1
                    keyword_search.save()

        return queryset.distinct()



class PublicToolList(generics.ListCreateAPIView):
    queryset = Tool.objects.filter(status=ToolStatus.ACTIVE)
    serializer_class = PublicToolListSerializer
    permission_classes = [CustomIdentityHeaderPermission]
    pagination_class = CustomPagination10

    def get_queryset(self):
        queryset = (
            self.queryset.prefetch_related(
                Prefetch(
                    "toolsconnector_set",
                    queryset=ToolsConnector.objects.select_related("rating", "feature"),
                ),
                Prefetch(
                    "toolscategoryconnector_set",
                    queryset=ToolsCategoryConnector.objects.select_related(
                        "category", "subcategory"
                    ),
                ),
            )
        )

        queryset = queryset.annotate(
            average_ratings=Avg("toolsconnector__rating__rating")
        ).order_by("-created_at")

        search = self.request.query_params.get("search", None)
        subcategory = self.request.query_params.get("subcategory", [])
        features = self.request.query_params.get("features", [])
        ordering_param = self.request.query_params.get("ordering", None)
        time_range = self.request.query_params.get("time_range", None)
        trending = self.request.query_params.get("trending", None)
        pricing = self.request.query_params.get("pricing", None)
        min_love_count = self.request.query_params.get("min_love", None)
        max_love_count = self.request.query_params.get("max_love", None)
        top_tools = self.request.query_params.get("top_tools", False)
        deals = self.request.query_params.get("deals", None)


        if deals and deals == "true":
            queryset = queryset.filter(is_deal=True)

        if top_tools:
            top_hundred_tools_ids = TopHundredTools.objects.values_list(
                "feature_tool_id", flat=True
            )
            queryset = (
                queryset.filter(id__in=top_hundred_tools_ids)
                .annotate(
                    priority_gt_zero=Case(
                        When(tophundredtools__priority__gt=0, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    ),
                )
                .order_by(
                    # Order by is_add=True
                    "-tophundredtools__is_add",
                    # Then by priority greater than 0
                    "-priority_gt_zero",
                    # Then by is_add=False and priority=0
                    "tophundredtools__is_add",
                    "tophundredtools__priority",
                )
            )

        if search is not None:
            search_words = [
                word.strip() for word in search.split(" ") if len(word.strip()) >= 2
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
                from django.db.models import Exists, OuterRef

                queryset = (
                    queryset.filter(q_object)
                    .annotate(
                        connected_feature_tools=Exists(
                            ToolsConnector.objects.filter(
                                tool_id=OuterRef("id"), feature_id__isnull=False
                            )
                        )
                    )
                    .order_by("-connected_feature_tools", "-created_at")
                )

                # Save the search keyword and associate it with the user if authenticated
                user = self.request.user
                keyword, created = Keyword.objects.get_or_create(name=search)

                if user.is_authenticated:
                    keyword_search = KeywordSearch.objects.filter(
                        keyword=keyword
                    ).first()

                    if not keyword_search:
                        keyword_search = KeywordSearch.objects.create(
                            keyword=keyword, user=user
                        )
                    keyword_search.search_count += 1
                    keyword_search.save()

                else:
                    keyword_search = KeywordSearch.objects.filter(
                        keyword=keyword
                    ).first()
                    if not keyword_search:
                        keyword_search = KeywordSearch.objects.create(keyword=keyword)
                    keyword_search.search_count += 1
                    keyword_search.save()

        if time_range:
            now = timezone.now()

            if time_range == "today":
                start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
                queryset = queryset.filter(
                    created_at__gte=start_date, created_at__lt=now
                )

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

        if trending:
            now = timezone.now()

            if trending == "today":
                start_date = date.today()
                queryset = (
                    queryset.annotate(
                        total_saved_tools=Count(
                            "save_tool", filter=Q(save_tool__created_at__gte=start_date)
                        )
                    )
                    .filter(total_saved_tools__gt=3)
                    .order_by("-total_saved_tools")
                )

            if trending == "this_week":
                start_date = now - timedelta(days=now.weekday())
                queryset = (
                    queryset.annotate(
                        total_saved_tools=Count(
                            "save_tool", filter=Q(save_tool__created_at__gte=start_date)
                        )
                    )
                    .filter(total_saved_tools__gt=3)
                    .order_by("-total_saved_tools")
                )

            elif trending == "this_month":
                start_date = now.replace(day=1)
                queryset = (
                    queryset.annotate(
                        total_saved_tools=Count(
                            "save_tool", filter=Q(save_tool__created_at__gte=start_date)
                        )
                    )
                    .filter(total_saved_tools__gt=3)
                    .order_by("-total_saved_tools")
                )

            elif trending == "last_month":
                last_month_end = now.replace(day=1) - timedelta(days=1)
                last_month_start = last_month_end.replace(day=1)
                queryset = (
                    queryset.annotate(
                        total_saved_tools=Count(
                            "save_tool",
                            filter=Q(
                                save_tool__created_at__range=(
                                    last_month_start,
                                    last_month_end,
                                )
                            ),
                        )
                    )
                    .filter(total_saved_tools__gt=3)
                    .order_by("-total_saved_tools")
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
            if ordering_param == "most_popular":
                queryset = queryset.order_by("-save_count")
            elif ordering_param == "most_rated":
                queryset = queryset.order_by("-average_ratings")

            elif ordering_param == "newest":
                queryset = queryset.order_by("-created_at")

            elif ordering_param == "verified":
                queryset = queryset.order_by("-is_verified", "-created_at")

        pricing_options = {
            "free": PricingKind.FREE,
            "freemium": PricingKind.FREEMIUM,
            "free_trial": PricingKind.FREE_TRIAL,
            "premium": PricingKind.PREMIUM,
            "contact_for_pricing": PricingKind.CONTACT_FOR_PRICING,
        }

        if pricing and pricing in pricing_options:
            queryset = queryset.filter(pricing=pricing_options[pricing]).order_by(
                "-created_at"
            )

        if min_love_count and max_love_count:
            queryset = queryset.filter(
                save_count__range=(min_love_count, max_love_count)
            )
        if min_love_count and not max_love_count:
            queryset = queryset.filter(save_count__gte=min_love_count)
        if max_love_count and not min_love_count:
            queryset = queryset.filter(save_count__lte=max_love_count)

        filters_applied = any([search, subcategory, features, ordering_param, time_range, trending, pricing, min_love_count, max_love_count, top_tools, deals])
        if filters_applied:
            queryset = queryset.order_by(
                "-is_featured",
                "-is_category_featured",
                "-created_at"
            )
        else:
            queryset = queryset.order_by("-is_featured","-created_at")

        return queryset.distinct()


class PublicToolDetail(generics.RetrieveUpdateAPIView):
    queryset = Tool.objects.filter()
    serializer_class = PublicTooDetailSerializer
    permission_classes = [CustomIdentityHeaderPermission]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            average_ratings=Avg("toolsconnector__rating__rating")
        )
        return queryset.distinct()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        alternative_tool = self.get_alternative_tool(instance)
        serializer = self.get_serializer(instance)
        data = serializer.data
        if alternative_tool:
            alternative_serializer = PublicToolListSerializer(
                alternative_tool, context={"request": request}
            )
            data["alternative_tool"] = alternative_serializer.data

        else:
            data["alternative_tool"] = {}

        queryset = self.get_queryset()
        tool_position = list(queryset).index(instance)
        data["index_no"] = tool_position
        return Response(data)

    def get_alternative_tool(self, current_tool):
        try:
            # current tool category
            category = current_tool.toolscategoryconnector_set.first().category
            queryset = (
                Tool.objects.annotate(total_save_count=Count("save_tool"))
                .filter(toolscategoryconnector__category=category)  # Filter by category
                .order_by("-total_save_count")
            )

            current_position = list(queryset).index(current_tool)

            alternative_position = current_position + 1
            if alternative_position < len(queryset):
                alternative_tool = queryset[alternative_position]
                return alternative_tool
            return None

        except:
            return None


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

            if time_range == "today":
                start_date = date.today()
                queryset = (
                    queryset.annotate(
                        total_saved_tools=Count(
                            "save_tool", filter=Q(save_tool__created_at__gte=start_date)
                        )
                    )
                    .filter(total_saved_tools__gt=3)
                    .order_by("-total_saved_tools")
                )

            if time_range == "this_week":
                start_date = now - timedelta(days=now.weekday())
                queryset = (
                    queryset.annotate(
                        total_saved_tools=Count(
                            "save_tool", filter=Q(save_tool__created_at__gte=start_date)
                        )
                    )
                    .filter(total_saved_tools__gt=3)
                    .order_by("-total_saved_tools")
                )

            elif time_range == "this_month":
                start_date = now.replace(day=1)
                queryset = (
                    queryset.annotate(
                        total_saved_tools=Count(
                            "save_tool", filter=Q(save_tool__created_at__gte=start_date)
                        )
                    )
                    .filter(total_saved_tools__gt=3)
                    .order_by("-total_saved_tools")
                )

            elif time_range == "last_month":
                last_month_end = now.replace(day=1) - timedelta(days=1)
                last_month_start = last_month_end.replace(day=1)
                queryset = (
                    queryset.annotate(
                        total_saved_tools=Count(
                            "save_tool",
                            filter=Q(
                                save_tool__created_at__range=(
                                    last_month_start,
                                    last_month_end,
                                )
                            ),
                        )
                    )
                    .filter(total_saved_tools__gt=3)
                    .order_by("-total_saved_tools")
                )

        return queryset


class PublicTrendingToolDetail(generics.RetrieveAPIView):
    queryset = Tool.objects.filter(status=ToolStatus.ACTIVE)
    serializer_class = PublicTrendingToolListSerializer
    permission_classes = [CustomIdentityHeaderPermission]
    lookup_field = "slug"


class PublicSubCategoryToolList(generics.ListAPIView):
    queryset = Tool.objects.filter(status=ToolStatus.ACTIVE)
    serializer_class = PublicSubCategoryToolSerializer
    permission_classes = [CustomIdentityHeaderPermission]
    # pagination_class = CustomPagination10

    def get_queryset(self):
        slug = self.kwargs.get("subcategory_slug", None)

        queryset = (
            self.queryset.filter(toolscategoryconnector__subcategory__slug=slug)
            .annotate(average_ratings=Avg("toolsconnector__rating__rating"))
            .order_by("-created_at")
        )

        # query params
        search = self.request.query_params.get("search", None)
        features = self.request.query_params.get("features", [])
        ordering_param = self.request.query_params.get("ordering", None)
        time_range = self.request.query_params.get("time_range", None)
        trending = self.request.query_params.get("trending", None)

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
                    keyword_search = KeywordSearch.objects.filter(
                        keyword=keyword
                    ).first()

                    if not keyword_search:
                        keyword_search = KeywordSearch.objects.create(
                            keyword=keyword, user=user
                        )
                    keyword_search.search_count += 1
                    keyword_search.save()

                else:
                    keyword_search = KeywordSearch.objects.filter(
                        keyword=keyword
                    ).first()
                    if not keyword_search:
                        keyword_search = KeywordSearch.objects.create(keyword=keyword)
                    keyword_search.search_count += 1
                    keyword_search.save()

        if time_range:
            now = timezone.now()

            if time_range == "today":
                start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
                queryset = queryset.filter(
                    created_at__gte=start_date, created_at__lt=now
                )

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

        if features:
            features = features.split(",")
            queryset = queryset.filter(toolsconnector__feature__slug__in=features)

        if ordering_param:
            if ordering_param == "most_loved":
                queryset = queryset.order_by("-save_count")
            elif ordering_param == "average_ratings":
                queryset = queryset.order_by("-average_ratings")

            elif ordering_param == "created_at":
                queryset = queryset.order_by("-created_at")

        if trending:
            now = timezone.now()

            if trending == "today":
                start_date = date.today()
                queryset = (
                    queryset.annotate(
                        total_saved_tools=Count(
                            "save_tool", filter=Q(save_tool__created_at__gte=start_date)
                        )
                    )
                    .filter(total_saved_tools__gt=3)
                    .order_by("-total_saved_tools")
                )

            if trending == "this_week":
                start_date = now - timedelta(days=now.weekday())
                queryset = (
                    queryset.annotate(
                        total_saved_tools=Count(
                            "save_tool", filter=Q(save_tool__created_at__gte=start_date)
                        )
                    )
                    .filter(total_saved_tools__gt=3)
                    .order_by("-total_saved_tools")
                )

            elif trending == "this_month":
                start_date = now.replace(day=1)
                queryset = (
                    queryset.annotate(
                        total_saved_tools=Count(
                            "save_tool", filter=Q(save_tool__created_at__gte=start_date)
                        )
                    )
                    .filter(total_saved_tools__gt=3)
                    .order_by("-total_saved_tools")
                )

            elif trending == "last_month":
                last_month_end = now.replace(day=1) - timedelta(days=1)
                last_month_start = last_month_end.replace(day=1)
                queryset = (
                    queryset.annotate(
                        total_saved_tools=Count(
                            "save_tool",
                            filter=Q(
                                save_tool__created_at__range=(
                                    last_month_start,
                                    last_month_end,
                                )
                            ),
                        )
                    )
                    .filter(total_saved_tools__gt=3)
                    .order_by("-total_saved_tools")
                )

        return queryset.distinct()


class PublicSubCategoryToolListExtraField(APIView):
    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get("subcategory_slug", None)
        subcategory = generics.get_object_or_404(
            SubCategory.objects.filter(), slug=slug
        )
        total_tool = Tool.objects.filter(toolscategoryconnector__subcategory__slug=slug)

        return Response(
            {
                "title": subcategory.title,
                "text": subcategory.text,
                "description": subcategory.description,
                "total": total_tool.count(),
            }
        )


class PublicCodeVerifyApi(APIView):
    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get("slug", None)
        tool = generics.get_object_or_404(Tool.objects.filter(), slug=slug)
        code = tool.verification_code
        url = tool.website_url

        if url == "":
            return Response(
                {"detail": "Wrong URL or you didn't fill up your website link!"},
                status=400,
            )

        if tool.is_verified:
            return Response(
                {"detail": "You have already been verified!"},
                status=400,
            )

        commitment = check_code_presence(url, code)

        if commitment:
            tool.verified_status = VerifiedStatus.PENDING
            tool.save()
            return Response({"detail": "Verification request has sent!"})

        return Response(
            {"detail": "Verification failed. Something went wrong!"},
            status=500,
        )


class PublicSuggessionList(generics.ListAPIView):
    queryset = Tool.objects.filter(status=ToolStatus.ACTIVE, is_suggession=True)
    serializer_class = PublicToolListSerializer
    permission_classes = []


class PublicTopHundredToolsList(generics.ListAPIView):
    queryset = (
        TopHundredTools.objects.select_related("feature_tool")
        .filter()
        .order_by("-is_add", "-created_at")
    )
    serializer_class = PrivateTopHundredToolsSerializer
    permission_classes = []


class PublicTopHundredToolsDetail(generics.RetrieveAPIView):
    queryset = (
        TopHundredTools.objects.select_related("feature_tool")
        .filter()
        .order_by("-is_add", "-created_at")
    )
    serializer_class = PrivateTopHundredToolsSerializer
    permission_classes = []
    lookup_field = "slug"


class PublicBestAlternativeToolList(generics.ListAPIView):
    queryset = BestAlternativeTool.objects.filter()
    serializer_class = PrivateBestAlternativeToolSerializer
    permission_classes = []

    def get_queryset(self):
        from rest_framework import status
        from rest_framework.response import Response

        category_slug = self.kwargs.get("category_slug", None)
        if category_slug is None:
            return Response(
                {"detail": "Category slug is missing"}, status=status.HTTP_404_NOT_FOUND
            )

        return self.queryset.filter(category__slug=category_slug)


class PublicBestAlternativeToolDetail(generics.RetrieveAPIView):
    queryset = BestAlternativeTool.objects.filter()
    serializer_class = PrivateBestAlternativeToolSerializer
    permission_classes = []
    lookup_field = "slug"

    def get_object(self):
        from rest_framework.generics import get_object_or_404

        category_slug = self.kwargs.get("category_slug", None)
        slug = self.kwargs.get("slug", None)

        best_al_tool = get_object_or_404(
            self.queryset, category__slug=category_slug, slug=slug
        )

        return best_al_tool
