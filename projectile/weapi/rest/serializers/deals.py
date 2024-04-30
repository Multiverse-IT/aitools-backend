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

    # def create(self, validated_data):
    #     if not "tool_slug" in validated_data:
    #         raise ValidationError({"detail":"tool slug nedded to be provide!"})
    #     tool = validated_data.pop("tool_slug")
    #     discout = validated_data.get("discout", 0)
    #     coupon = validated_data.get("coupon", None)

    #     # Use get_or_create method to either get an existing object or create a new one
    #     deal_tool, created = Deal.objects.get_or_create(
    #         deal_tool_slug=tool,
    #         user=self.context["request"].user,
    #         defaults=validated_data
    #     )
    def create(self, validated_data):
        if "tool_slug" not in validated_data:
            raise ValidationError({"detail": "Tool slug needs to be provided!"})

        tool_slug = validated_data.pop("tool_slug")
        # discout = validated_data.get("discout", 0)
        coupon = validated_data.get("coupon", None)

        # Check if the tool exists
        try:
            tool = tool_slug
        except Tool.DoesNotExist:
            raise ValidationError({"detail": f"Tool with slug '{tool_slug}' does not exist!"})

        # Use get_or_create method to either get an existing object or create a new one
        deal_tool, created = Deal.objects.get_or_create(
            deal_tool=tool,
            user=self.context["request"].user,
            defaults=validated_data
        )

        tool.discout = validated_data.get("discout", 0)
        if coupon is not None:
            tool.coupon = coupon

        tool.is_deal = True
        tool.save()

        return deal_tool

    def update(self, instance, validated_data):
        if "tool_slug" in validated_data:
            tool = validated_data.pop("tool_slug")
            validated_data["deal_tool"] = tool

        # if "coupon" in validated_data:
        #     coupon = validated_data.get("coupon", None)
        #     if coupon is not None:
        #         instance.deal_tool.coupon = coupon
        #         instance.deal_tool.save()

        # discout = validated_data.get("discout", 0)
        # if discout > 0:
        #     instance.deal_tool.discout = discout
        #     instance.deal_tool.save()

        if "coupon" in validated_data:
            instance.deal_tool.coupon = validated_data["coupon"]
        if "discout" in validated_data:
            instance.deal_tool.discout = validated_data["discout"]

        instance.deal_tool.save()

        return super().update(instance, validated_data)