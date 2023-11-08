from catalogio.choices import RequestToolStatus, ToolKind, ToolStatus
from catalogio.models import (
    Category,
    Feature,
    SubCategory,
    Tool,
    ToolRequest,
    ToolsCategoryConnector,
    ToolsConnector,
)
from common.serializers import (
    CategorySlimSerializer,
    FeatureSlimSerializer,
    SubCategorySlimSerializer,
    RatingSlimSerializer,
)
from rest_framework import serializers


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
            "feature_slugs",
            "feature",
            "status",
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
            "created_at",
        ]

        read_only_fields = ["uid", "created_at"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['feature'] = [feature for feature in data['feature'] if feature]
        data['ratings'] = [rating for rating in data['ratings'] if rating]
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

        return tool

    def update(self, instance, validated_data):
        feature_slugs = validated_data.pop("feature_slugs", None)
        category_slug = validated_data.pop("category_slug", None)
        subcategory_slugs = validated_data.pop("subcategory_slugs", [])

        if feature_slugs:
            self._extracted_from_update_9(feature_slugs, instance)

        # Update category if category_slug is provided
        if category_slug:
            instance.category = category_slug
            instance.save()

        # Update subcategories if subcategory_slugs are provided
        if subcategory_slugs:
            # First, remove existing subcategory connectors for this tool
            subcategory_connectors = instance.toolscategoryconnector_set.filter()
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


class ToolRequestDetalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToolRequest
        fields = ("status",)

    def update(self, instance, validated_data):
        status = validated_data.get("status", None)

        if status == RequestToolStatus.APPROVED:
            instance.status = ToolStatus.ACTIVE
            instance.save()
            
        return super().update(instance, validated_data)
