from catalogio.choices import ToolKind
from catalogio.models import (
    Category,
    Feature,
    SubCategory,
    Tool,
    ToolsCategoryConnector,
    ToolsConnector,
)
from rest_framework import serializers

from common.serializers import CategorySlimSerializer, SubCategorySlimSerializer


class ToolListSerializer(serializers.ModelSerializer):
    feature_slug = serializers.SlugRelatedField(
        slug_field="slug", queryset=Feature.objects.all(), required=False, many=False
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

    class Meta:
        model = Tool
        fields = [
            "uid",
            "slug",
            "name",
            "is_verified",
            "pricing",
            "categories",
            "description",
            "is_editor",
            "is_trending",
            "is_new",
            "save",
            "meta_title",
            "meta_description",
            "image",
            "is_indexed",
            "feature_slug",
            "status",
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

        read_only_fields = ["uid", "created_at"]

    def create(self, validated_data):
        feature = validated_data.pop("feature_slug", None)
        category = validated_data.pop("category_slug", None)
        subcategory_slugs = validated_data.pop("subcategory_slugs", [])

        tool = Tool.objects.create(**validated_data)

        if feature:
            feature_connector, _ = ToolsConnector.objects.get_or_create(
                tool=tool, feature=feature, kind=ToolKind.FEATURE
            )

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
                print("detail:", str(e))

        return tool
