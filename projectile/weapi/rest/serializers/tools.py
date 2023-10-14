from rest_framework import serializers

from catalogio.models import Tool


class ToolListSerializer(serializers.ModelSerializer):
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
            "status",
            "short_description",
            "canonical_url",
            "website_url",
            "linkedin_url",
            "facebook_url",
            "twitter_url",
            "created_at",
        ]

        read_only_fields = ["uid","created_at"]
