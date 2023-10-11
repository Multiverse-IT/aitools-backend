from rest_framework import serializers

from catalogio.models import Category, SubCategory


class CatetoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["uid", "slug", "title"]
        read_only_fields = ["__all__"]

class SubCatetoryListByCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ["uid", "slug", "title"]
        read_only_fields = ["__all__"]
