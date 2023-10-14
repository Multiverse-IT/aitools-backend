from catalogio.models import Category, SubCategory
from rest_framework import serializers


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
    class Meta:
        model = SubCategory
        fields = [
            "uid",
            "slug",
            "title",
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
