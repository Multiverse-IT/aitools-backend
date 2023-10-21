from rest_framework import serializers

from catalogio.choices import ToolKind
from catalogio.models import Feature, Tool, ToolsConnector


class ToolListSerializer(serializers.ModelSerializer):
    feature_slug = serializers.SlugRelatedField(
        slug_field="slug", queryset=Feature.objects.all(), required=False, many=False
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
            "feature_slug",
            "status",
            "short_description",
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
        tool = Tool.objects.create(**validated_data)

        if feature:
            feature_connector, _ = ToolsConnector.objects.get_or_create(
                tool=tool, feature=feature, kind=ToolKind.FEATURE
            )

        return tool
