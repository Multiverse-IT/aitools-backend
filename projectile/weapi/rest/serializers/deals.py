from rest_framework import serializers
from rest_framework.generics import ValidationError

from catalogio.models import Deal, Tool

from ..serializers.tools import ToolListSerializer


class PrivateDealsSerializer(serializers.ModelSerializer):
    tool_slug = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Tool.objects.filter(),
        write_only=True,
        required=False,
    )
    deal_tool = ToolListSerializer(read_only=True)

    class Meta:
        model = Deal
        fields = (
            "slug",
            "deal_tool",
            "is_top",
            "is_hot_deal",
            "coupon",
            "discout",
            "created_at",
            "updated_at",
            "tool_slug",
        )
        read_only_fields = ["slug", "created_at", "updated_at"]

    def create(self, validated_data):
        if "tool_slug" not in validated_data:
            raise ValidationError({"detail": "Tool slug needs to be provided!"})

        tool_slug = validated_data.pop("tool_slug")
        # Check if the tool exists
        try:
            tool = tool_slug
        except Tool.DoesNotExist:
            raise ValidationError(
                {"detail": f"Tool with slug '{tool_slug}' does not exist!"}
            )

        # Use get_or_create method to either get an existing object or create a new one
        deal_tool, created = Deal.objects.get_or_create(
            deal_tool=tool, user=self.context["request"].user, defaults=validated_data
        )

        return deal_tool

    def update(self, instance, validated_data):
        if "tool_slug" in validated_data:
            tool = validated_data.pop("tool_slug")
            validated_data["deal_tool"] = tool


        return super().update(instance, validated_data)
