from rest_framework import serializers


class CategorySlimSerializer(serializers.Serializer):
    slug = serializers.CharField(source="category.slug", read_only=True)
    title = serializers.CharField(source="category.title", read_only=True)
    meta_title = serializers.CharField(
        source="category.meta_title", read_only=True, required=False
    )
    meta_description = serializers.CharField(
        source="category.meta_description", read_only=True, required=False
    )
    is_indexed = serializers.CharField(source="category.is_indexed", read_only=True)
    canonical_url = serializers.CharField(
        source="category.canonical_url", read_only=True, required=False
    )


class SubCategorySlimSerializer(serializers.Serializer):
    slug = serializers.CharField(source="subcategory.slug", read_only=True)
    title = serializers.CharField(source="subcategory.title", read_only=True)
    meta_title = serializers.CharField(
        source="subcategory.meta_title", read_only=True, required=False
    )
    meta_description = serializers.CharField(
        source="subcategory.meta_description", read_only=True, required=False
    )
    is_indexed = serializers.CharField(source="subcategory.is_indexed", read_only=True)
    canonical_url = serializers.CharField(
        source="subcategory.canonical_url", read_only=True, required=False
    )
