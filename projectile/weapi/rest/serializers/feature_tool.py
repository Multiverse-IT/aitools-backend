from rest_framework import serializers

from catalogio.models import FeatureTool, Tool

from ..serializers.tools import ToolListSerializer

class PrivateFeatureToolSerializer(serializers.ModelSerializer):
    tool_slugs = serializers.ListField(
        write_only=True, required=False, child=serializers.CharField()
    )
    class Meta:
        model = FeatureTool
        fields = ("slug", "tool", "created_at", "updated_at", "tool_slugs")

        read_only_fields = ["created_at", "updated_at"]

    def create(self, validated_data):
        user=self.context["request"].user
        tool_slugs = validated_data.pop("tool_slugs", None)
        tools = Tool.objects.filter(slug__in=tool_slugs)
        feature_tool = FeatureTool.objects.create(user=user, **validated_data)
        feature_tool.tool = ToolListSerializer(tools, many=True).data
        feature_tool.save()
        
        return feature_tool
    
    def update(self, instance, validated_data):
        tool_slugs = validated_data.pop("tool_slugs", None)
        instance.tool = []
        instance.save()
        tools = Tool.objects.filter(slug__in=tool_slugs)
        instance.tool = ToolListSerializer(tools, many=True).data
        instance.save()

        return instance
    