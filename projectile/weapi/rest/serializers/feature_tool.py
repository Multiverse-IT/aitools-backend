from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from catalogio.models import FeatureTool, Tool, BestAlternativeTool, Category

from ..serializers.tools import ToolListSerializer
from common.serializers import CategorySlimSerializerForBestAlternative

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


class PrivateBestAlternativeToolSerializer(serializers.ModelSerializer):
    tool_uids = serializers.ListField(
        write_only = True,
        child =serializers.UUIDField()
    )
    tool = ToolListSerializer(read_only=True)
    category_slug = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.filter(),
        write_only=True,
    )
    category = CategorySlimSerializerForBestAlternative(read_only=True)
    class Meta:
        model = BestAlternativeTool
        fields = [
            "uid",
            "slug",
            "tool",
            "tool_uids",
            "category_slug",
            "category",
            "remarks",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["slug", "tool", "created_at", "updated_at"]


    def create(self, validated_data):
        request = self.context["request"]
        tool_uids = validated_data.pop("tool_uids")
        category = validated_data.pop("category_slug")
        print("category ;;;;;;;;;;;;;;;:", category)

        removal_tools = BestAlternativeTool.objects.filter(tool__uid__in = tool_uids)
        removal_tools.delete()

        tools_to_add_to_best_alternative = Tool.objects.filter(uid__in = tool_uids).distinct()

        tools_list = []
        try:
            for item in tools_to_add_to_best_alternative:
                tools_list.append(
                    BestAlternativeTool(
                        tool=item,
                        user = request.user,
                        category = category,
                        **validated_data
                    )
                )
            BestAlternativeTool.objects.bulk_create(tools_list)

        except Exception as e:
            raise ValidationError({"error": str(e)})


        return validated_data
