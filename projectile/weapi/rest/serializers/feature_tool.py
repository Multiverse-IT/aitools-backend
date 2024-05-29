from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from catalogio.models import FeatureTool, Tool, BestAlternativeTool, Category, SubCategory

from ..serializers.tools import ToolListSerializer
from common.serializers import CategorySlimSerializerForBestAlternative

class PrivateFeatureToolSerializer(serializers.ModelSerializer):
    tool_slug = serializers.SlugRelatedField(
        slug_field="slug", queryset=Tool.objects.filter(), write_only = True,
    )
    sub_category_slug = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=SubCategory.objects.filter(),
        write_only=True, required=False, allow_null=True, allow_empty=True
    )
    feature_tool = ToolListSerializer(read_only=True)
    class Meta:
        model = FeatureTool
        fields = ("slug", "feature_tool","custom_field", "in_pages", "created_at", "updated_at","sub_category_slug", "tool_slug")
        read_only_fields = ["slug","created_at", "updated_at"]

    def create(self, validated_data):
        tool = validated_data.pop("tool_slug")
        sub_category = validated_data.pop("sub_category_slug", None)

        feature_tool = FeatureTool.objects.create(
            feature_tool=tool,
            user=self.context["request"].user,
            **validated_data
        )

        if sub_category is not None:
            feature_tool.subcategory = sub_category
            feature_tool.save()

            feature_tool.feature_tool.is_category_featured = True
            feature_tool.feature_tool.save()
        else:
            tool.is_featured = True
            tool.save()
        return feature_tool


class PrivateBestAlternativeToolSerializer(serializers.ModelSerializer):
    tool_uids = serializers.ListField(
        write_only = True,
        child =serializers.UUIDField(),
        required=False,
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
        tool_uids = validated_data.pop("tool_uids", None)
        if tool_uids is None:
            raise ValidationError({"error": "tool uids are required."})

        category = validated_data.pop("category_slug")

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


    def update(self, instance, validated_data):
        category = validated_data.pop("category_slug")
        validated_data['category'] = category
        return super().update(instance, validated_data)
