from catalogio.models import Category, SubCategory
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

class CatetoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "uid",
            "slug",
            "title",
            "meta_title",
            "meta_description",
            "canonical_url",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["uid", "created_at", "updated_at"]


class SubCatetoryListDetailSerializer(serializers.ModelSerializer):
    category_slug = serializers.SlugRelatedField(
        "slug", queryset=Category.objects.filter(), write_only=True, required=True
    )
    category = CatetoryListSerializer(read_only=True)

    class Meta:
        model = SubCategory
        fields = [
            "uid",
            "slug",
            "title",
            "category_slug",
            "category",
            "meta_title",
            "meta_description",
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
        category_slug = validated_data.pop("category_slug", None)
        return SubCategory.objects.create(category=category_slug, **validated_data)
