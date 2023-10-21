from rest_framework import serializers

from catalogio.models import Rating, Tool, ToolsConnector
# from catalogio.choices import 

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
            rating_connector, _ = ToolsConnector.objects.create(
                tool=tool, rating=rating
            )
        return rating
