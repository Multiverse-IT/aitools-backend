from rest_framework import serializers

from catalogio.choices import RequestToolStatus, ToolKind, ToolStatus, VerifiedStatus
from catalogio.models import (
    Category,
    Feature,
    SubCategory,
    Tool,
    ToolsCategoryConnector,
    ToolsConnector,
    TopHundredTools,
    FeatureTool
)
from common.serializers import (
    CategorySlimSerializer,
    FeatureSlimSerializer,
    SubCategorySlimSerializer,
    RatingSlimSerializer,
)


class ToolListSerializer(serializers.ModelSerializer):
    feature_slugs = serializers.ListField(
        write_only=True, required=False, child=serializers.CharField()
    )
    category_slug = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all(),
        write_only=True,
        required=False,
    )
    subcategory_slugs = serializers.ListField(
        write_only=True, required=False, child=serializers.CharField()
    )
    category = CategorySlimSerializer(
        source="toolscategoryconnector_set.first", read_only=True
    )
    sub_category = SubCategorySlimSerializer(
        source="toolscategoryconnector_set", many=True, read_only=True
    )
    feature = FeatureSlimSerializer(
        source="toolsconnector_set", many=True, read_only=True
    )
    ratings = RatingSlimSerializer(
        source="toolsconnector_set", many=True, read_only=True
    )

    class Meta:
        model = Tool
        fields = [
            "uid",
            "slug",
            "name",
            "is_verified",
            "verified_status",
            "pricing",
            "categories",
            "description",
            "is_editor",
            "is_trending",
            "is_new",
            "is_featured",
            "is_category_featured",
            "do_follow_website",
            "save_count",
            "meta_title",
            "meta_description",
            "image",
            "logo",
            "logo_alt",
            "price",
            "is_deal",
            "is_suggession",
            "alt",
            "verification_code",
            "is_noindex",
            "do_sponsor_website",
            "focus_keyword",
            "feature_slugs",
            "feature",
            "status",
            "discout",
            "coupon",
            "requested",
            "short_description",
            "category_slug",
            "category",
            "subcategory_slugs",
            "sub_category",
            "ratings",
            "canonical_url",
            "website_url",
            "linkedin_url",
            "facebook_url",
            "twitter_url",
            "instagram_url",
            "email_url",
            "tiktok_url",
            "github_url",
            "youtube_url",
            "discoard_url",
            "pricing_url",
            "created_at",
            "updated_at"
        ]

        read_only_fields = ["uid", "is_deal", "created_at", "coupon","discout"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["feature"] = [feature for feature in data["feature"] if feature]
        data["ratings"] = [rating for rating in data["ratings"] if rating]
        return data

    def create(self, validated_data):
        feature_slugs = validated_data.pop("feature_slugs", None)
        category = validated_data.pop("category_slug", None)
        subcategory_slugs = validated_data.pop("subcategory_slugs", [])

        tool = Tool.objects.create(**validated_data)

        if feature_slugs:
            self._extracted_from_update_9(feature_slugs, tool)

        if category and subcategory_slugs:
            try:
                connectors = [
                    ToolsCategoryConnector(
                        tool=tool,
                        category=category,
                        subcategory=SubCategory.objects.get(slug=slug),
                    )
                    for slug in subcategory_slugs
                ]
                ToolsCategoryConnector.objects.bulk_create(connectors)

            except Exception as e:
                print("detail:", e)

        tool.updated_at = tool.created_at
        tool.save()

        return tool

    def update(self, instance, validated_data):
        feature_slugs = validated_data.pop("feature_slugs", None)
        category_slug = validated_data.pop("category_slug", None)
        subcategory_slugs = validated_data.pop("subcategory_slugs", [])

        if feature_slugs:
            self._extracted_from_update_9(feature_slugs, instance)

        # Update category if category_slug is provided
        if category_slug:
            try:
                # instance.category = category_slug
                # instance.save()
                connector = instance.toolscategoryconnector_set.first()
                if connector:
                    connector.category = category_slug
                    connector.save()
                else:
                    connector = ToolsCategoryConnector.objects.create(tool=instance, category=category_slug)

            except Category.DoesNotExist:
                print("Category not found")


        # Update subcategories if subcategory_slugs are provided
        if subcategory_slugs:
            # First, remove existing subcategory connectors for this tool
            subcategory_connectors = instance.toolscategoryconnector_set.filter()
            if subcategory_connectors.exists():
                category = subcategory_connectors.first().category
                subcategory_connectors.delete()

                # Then, create new subcategory connectors for the provided subcategory slugs
                connectors = [
                    ToolsCategoryConnector(
                        tool=instance,
                        category=category,
                        subcategory=SubCategory.objects.get(slug=slug),
                    )
                    for slug in subcategory_slugs
                ]
                ToolsCategoryConnector.objects.bulk_create(connectors)

        return super().update(instance, validated_data)

    def _extracted_from_update_9(self, feature_slugs, tool):
        # features = ToolsConnector.objects.filter(
        #     feature__slug__in=feature_slugs, kind=ToolKind.FEATURE
        # ).delete()
        # n = tool.toolsconnector_set.filter().delete()
        feature_connectors = tool.toolsconnector_set.filter(
            feature__isnull=False
        ).delete()

        connectors = [
            ToolsConnector(
                tool=tool,
                feature=Feature.objects.filter(slug=slug).first(),
                kind=ToolKind.FEATURE,
            )
            for slug in feature_slugs
        ]
        ToolsConnector.objects.bulk_create(connectors)


class ToolRequestDetailSerializer(serializers.ModelSerializer):
    request_status = serializers.ChoiceField(
        choices=RequestToolStatus.choices, write_only=True
    )

    class Meta:
        model = Tool
        fields = ("status", "request_status")
        read_only_fields = ["status"]

    def update(self, instance, validated_data):
        from django.utils import timezone
        status = validated_data.pop("request_status", None)
        if status == RequestToolStatus.APPROVED:
            instance.status = ToolStatus.ACTIVE
            instance.is_new = True
            instance.created_at = timezone.now()
            instance.save()
            instance.updated_at = instance.created_at
            instance.save()

        return super().update(instance, validated_data)


class ToolWithVerifiedStatus(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = [
            "is_verified",
            "verified_status",
            "created_at",
        ]
        read_only_fields = ["is_verified", "created_at"]

    def update(self, instance, validated_data):
        status = validated_data.get("verified_status", None)
        if status == VerifiedStatus.APPROVED:
            instance.is_verified = True
            instance.save()
        return super().update(instance, validated_data)


class PrivateTopHundredToolsSerializer(serializers.ModelSerializer):
    tool_slugs = serializers.ListField(
        write_only=True, child=serializers.CharField(), required=False
    )
    tool = ToolListSerializer(source="feature_tool", read_only=True)

    class Meta:
        model = TopHundredTools
        fields = [
            "uid",
            "slug",
            "tool",
            "tool_slugs",
            "is_add",
            "priority",
            "created_at",
            "updated_at"
        ]

    def create(self, validated_data):
        request = self.context["request"]
        tool_slugs = validated_data.pop("tool_slugs")

        removable_tools = TopHundredTools.objects.filter(feature_tool__slug__in = tool_slugs)
        removable_tools.delete()

        tools_to_add_to_top_hundred_tools = Tool.objects.filter(slug__in = tool_slugs).distinct()

        tools_list = []
        try:
            for item in tools_to_add_to_top_hundred_tools:
                tools_list.append(
                    TopHundredTools(
                        feature_tool=item,
                        user = request.user,
                        **validated_data
                    )
                )
            TopHundredTools.objects.bulk_create(tools_list)

        except Exception as e:
            from rest_framework.exceptions import ValidationError

            raise ValidationError({"error": str(e)})


        return validated_data
