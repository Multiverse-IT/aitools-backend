from catalogio.choices import ToolKind, ToolStatus
from catalogio.models import (
    Category,
    SavedTool,
    SubCategory,
    Tool,
    ToolRequest,
    ToolsCategoryConnector,
)
from common.serializers import (
    CategorySlimSerializer,
    FeatureSlimSerializer,
    SubCategorySlimSerializer,
    RatingSlimSerializer
)
from rest_framework import serializers


class PublicToolListSerializer(serializers.ModelSerializer):
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
    ratings = RatingSlimSerializer(source="toolsconnector_set", many=True, read_only=True)
    class Meta:
        model = Tool
        fields = [
            "slug",
            "name",
            "is_verified",
            "pricing",
            "categories",
            "description",
            "is_editor",
            "is_trending",
            "is_new",
            "is_featured",
            "save_count",
            "meta_title",
            "meta_description",
            "image",
            "requested",
            "is_indexed",
            "feature_slugs",
            "feature",
            "status",
            "ratings",
            "short_description",
            "category_slug",
            "category",
            "subcategory_slugs",
            "sub_category",
            "canonical_url",
            "website_url",
            "linkedin_url",
            "facebook_url",
            "twitter_url",
            "created_at",
        ]

        read_only_fields = ["uid", "status","requested", "created_at"]

    def create(self, validated_data):
        user = self.context["request"].user
        feature_slugs = validated_data.pop("feature_slugs", None)
        category = validated_data.pop("category_slug", None)
        subcategory_slugs = validated_data.pop("subcategory_slugs", [])
        # requested = validated_data.get("requested")

        tool = Tool.objects.create(requested=True, status=ToolStatus.PENDING, **validated_data)
        
        if tool.requested == True:
            ToolRequest.objects.create(tool=tool, user=user)

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

        return tool


class PublicTooDetailSerializer(serializers.ModelSerializer):
    category = CategorySlimSerializer(
        source="toolscategoryconnector_set.first", read_only=True
    )
    sub_category = SubCategorySlimSerializer(
        source="toolscategoryconnector_set", many=True, read_only=True
    )
    feature = FeatureSlimSerializer(
        source="toolsconnector_set", many=True, read_only=True
    )
    ratings = RatingSlimSerializer(source="toolsconnector_set", many=True, read_only=True)

    class Meta:
        model = Tool
        fields = [
            "slug",
            "name",
            "is_verified",
            "pricing",
            "categories",
            "description",
            "is_editor",
            "is_trending",
            "is_new",
            "is_featured",
            "save_count",
            "meta_title",
            "meta_description",
            "image",
            "is_indexed",
            "feature",
            "status",
            "ratings",
            "short_description",
            "category",
            "sub_category",
            "canonical_url",
            "website_url",
            "linkedin_url",
            "facebook_url",
            "twitter_url",
            "created_at",
        ]

        read_only_fields = [
            "slug",
            "name",
            "is_verified",
            "pricing",
            "categories",
            "description",
            "is_editor",
            "is_trending",
            "is_new",
            "is_featured",
            "meta_title",
            "meta_description",
            "image",
            "is_indexed",
            "feature",
            "status",
            "short_description",
            "category",
            "sub_category",
            "canonical_url",
            "website_url",
            "linkedin_url",
            "facebook_url",
            "twitter_url",
            "created_at",
        ]

    def update(self, instance, validated_data):
        user = self.context["request"].user
        save_count = validated_data.get("save_count")

        if save_count is not None:
            instance.save_count = save_count
            instance.save()

            saved_tool_obj, _ = SavedTool.objects.get_or_create(
                save_tool=instance, user=user
            )

        return instance
