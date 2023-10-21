from rest_framework import serializers

from catalogio.choices import ToolKind
from catalogio.models import Rating, Tool, ToolsConnector

class RatingListDetaliSerializer(serializers.ModelSerializer):
    tool_slug = serializers.SlugRelatedField(
        slug_field="slug", queryset=Tool.objects.all(), many=False, required=False
    )
    class Meta:
        model = Rating
        fields = [
            "slug",
            "pros",
            "con",
            "review",
            "rating",
            "meta_title",
            "meta_description",
            "tool",
            "tool_slug",
            "canonical_url",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        tool = validated_data.pop("tool_slug", None)
        rating = Rating.objects.create(tool=tool, **validated_data)
        if tool:
            rating_connector, _ = ToolsConnector.objects.get_or_create(
                tool=tool, rating=rating, kind=ToolKind.RATING
            )
        return rating
