from rest_framework import serializers
from rest_framework.generics import ValidationError

from catalogio.models import Deal, Tool

from ..serializers.tools import ToolListSerializer

class PrivateDealsSerializer(serializers.ModelSerializer):
    tool_slug = serializers.SlugRelatedField(
        slug_field="slug", queryset=Tool.objects.filter(), write_only = True, required = False
    )
    deal_tool = ToolListSerializer(read_only=True)

    class Meta:
        model = Deal
        fields = ("slug", "deal_tool","is_top", "coupon", "discout", "created_at", "updated_at", "tool_slug")
        read_only_fields = ["slug","created_at", "updated_at"]

    def create(self, validated_data):
        if not "tool_slug" in validated_data:
            raise ValidationError({"detail":"tool slug nedded to be provide!"})
        tool = validated_data.pop("tool_slug")
        discout = validated_data.get("discout", 0)

        feature_tool = Deal.objects.create(
            deal_tool=tool,
            user=self.context["request"].user,
            **validated_data
        )

        if discout > 0:
            tool.discout = discout
            tool.save()

        return feature_tool

    def update(self, instance, validated_data):
        if "tool_slug" in validated_data:
            tool = validated_data.pop("tool_slug")
            validated_data["deal_tool"] = tool

        discout = validated_data.get("discout", 0)
        if discout > 0:
            instance.deal_tool.discout = discout
            instance.deal_tool.save()

        return super().update(instance, validated_data)