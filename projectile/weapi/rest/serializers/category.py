from rest_framework import serializers

from catalogio.models import Category, SubCategory, ToolsCategoryConnector
from common.serializers import CategorySlimSerializer, SubCategorySlimSerializer


class SubCategoriesSlimSerializer(serializers.Serializer):
    name = serializers.CharField(source="subcategory.title")
    total_tools = serializers.SerializerMethodField()

    def get_total_tools(self, obj):
        return obj.subcategory.toolscategoryconnector_set.count()


class CatetoryListSerializer(serializers.ModelSerializer):
    subCategories = SubCategoriesSlimSerializer(
        many=True, source="toolscategoryconnector_set", read_only=True
    )

    class Meta:
        model = Category
        fields = [
            "slug",
            "title",
            "subCategories",
            "meta_title",
            "meta_description",
            "is_indexed",
            "canonical_url",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["uid", "created_at", "updated_at"]


class SubCatetoryListDetailSerializer(serializers.ModelSerializer):
    category_slug = serializers.SlugRelatedField(
        "slug", queryset=Category.objects.filter(), write_only=True, required=True
    )
    category = CategorySlimSerializer(
        source="toolscategoryconnector_set.first", read_only=True
    )

    class Meta:
        model = SubCategory
        fields = [
            "slug",
            "title",
            "category_slug",
            "category",
            "meta_title",
            "meta_description",
            "is_indexed",
            "canonical_url",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "uid",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        category = validated_data.pop("category_slug", None)
        sub_category = SubCategory.objects.create(**validated_data)
        category_connector, _ = ToolsCategoryConnector.objects.get_or_create(
            category=category, subcategory=sub_category
        )
        return sub_category

    def update(self, instance, validated_data):
        category = validated_data.pop("category_slug", None)
        if category:
            category_connector = ToolsCategoryConnector.objects.filter(
                subcategory=instance
            ).first()
            category_connector.category = category
            category_connector.save()
        return super().update(instance, validated_data)
