from rest_framework import serializers

from catalogio.models import FeatureTool, Tool

from ..serializers.tools import ToolListSerializer

class PrivateFeatureToolSerializer(serializers.ModelSerializer):
    tool_slug = serializers.SlugRelatedField(
        slug_field="slug", queryset=Tool.objects.filter(), write_only = True,
    )
    feature_tool = ToolListSerializer(read_only=True)
    class Meta:
        model = FeatureTool
        fields = ("slug", "feature_tool","custom_field", "in_pages", "created_at", "updated_at", "tool_slug")
        read_only_fields = ["slug","created_at", "updated_at"]

    def create(self, validated_data):
        tool = validated_data.pop("tool_slug")
        feature_tool = FeatureTool.objects.create(
            feature_tool=tool,
            user=self.context["request"].user,
            **validated_data
        )
        return feature_tool