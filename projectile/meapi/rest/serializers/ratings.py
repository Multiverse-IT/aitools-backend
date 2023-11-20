from django.contrib.auth import get_user_model

from rest_framework import serializers

from catalogio.choices import ToolKind
from catalogio.models import Rating, Tool, ToolsConnector

from core.rest.serializers.users import UserSerializerList

User = get_user_model()

class MeRatingListDetaliSerializer(serializers.ModelSerializer):
    tool_slug = serializers.SlugRelatedField(
        slug_field="slug", queryset=Tool.objects.all(), many=False, required=False
    )
    user = UserSerializerList(read_only=True)
    class Meta:
        model = Rating
        fields = [
            "slug",
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
        identity = self.context["request"].headers.get("identity")
        user = User.objects.filter(id=identity).first()

        if not user:
            raise serializers.ValidationError({'detail': 'User not found.'})

        tool = validated_data.pop("tool_slug", None)
        rating = Rating.objects.create(user=user, **validated_data)
        if tool:
            rating_connector, _ = ToolsConnector.objects.get_or_create(
                tool=tool, rating=rating, kind=ToolKind.RATING
            )
        return rating
