from rest_framework import serializers

from catalogio.choices import ToolKind
from catalogio.models import Rating, Tool, ToolsConnector

from core.rest.serializers.users import UserSerializerList

class RatingListDetaliSerializer(serializers.ModelSerializer):
    tool_slug = serializers.SlugRelatedField(
        slug_field="slug", queryset=Tool.objects.all(), many=False, required=False
    )
    user = UserSerializerList(read_only=True)
    class Meta:
        model = Rating
        fields = [
            "pros",
            "cons",
            "review",
            "rating",
            "user",
            "meta_title",
            "meta_description",
            "tool_slug",
            "canonical_url",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        tool = validated_data.pop("tool_slug", None)
        rating = Rating.objects.create(**validated_data)
        if tool:
            rating_connector, _ = ToolsConnector.objects.get_or_create(
                tool=tool, rating=rating, kind=ToolKind.RATING
            )
        return rating
