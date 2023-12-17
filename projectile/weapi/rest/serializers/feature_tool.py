from rest_framework import serializers

from catalogio.models import FeatureTool, Tool

from ..serializers.tools import ToolListSerializer

class PrivateFeatureToolSerializer(serializers.ModelSerializer):
    tool_slugs = serializers.ListField(
        write_only=True, required=False, child=serializers.CharField()
    )
    tool = ToolListSerializer(read_only=True)

    class Meta:
        model = FeatureTool
        fields = ("slug", "tool", "created_at", "updated_at", "tool_slugs")

        read_only_fields = ["slug","created_at", "updated_at"]

    def create(self, validated_data):
        tool_slugs = validated_data.pop("tool_slugs", None)
        tools = Tool.objects.filter(slug__in=tool_slugs)

        if tools.exists():
            feature_tools = [
                FeatureTool(tool=tool, user=self.context["request"].user)
                for tool in tools if not FeatureTool.objects.filter(tool=tool).first()
            ]
            FeatureTool.objects.bulk_create(feature_tools)
       
        return validated_data
    
    def update(self, instance, validated_data):
        tool_slugs = validated_data.pop("tool_slugs", None)
        tools_to_remove = Tool.objects.filter(slug__in=tool_slugs)

        feature_tools = FeatureTool.objects.filter(tool__in=tools_to_remove)
        feature_tools.delete()
        tools = Tool.objects.filter(slug__in=tool_slugs)

        if tools.exists():
            feature_tools = [
                FeatureTool(tool=tool, user=self.context["request"].user)
                for tool in tools if not FeatureTool.objects.filter(tool=tool).first()
            ]
            FeatureTool.objects.bulk_create(feature_tools)
        return super().update(instance, validated_data)
    