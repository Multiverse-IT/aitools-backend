from rest_framework import serializers

from core.rest.serializers.users import UserSerializerList

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
    description = serializers.CharField(source="subcategory.description", read_only=True)

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


class FeatureSlimSerializer(serializers.Serializer):
    title = serializers.CharField(source="feature.title", read_only=True)
    slug = serializers.CharField(source="feature.slug", read_only=True)
    meta_title = serializers.CharField(source="feature.meta_title", read_only=True)
    meta_description = serializers.CharField(
        source="feature.meta_description", read_only=True
    )
    is_indexed = serializers.BooleanField(source="feature.is_indexed", read_only=True)
    canonical_url = serializers.URLField(source="feature.canonical_url", read_only=True)


class RatingSlimSerializer(serializers.Serializer):
    pros = serializers.CharField(source="rating.pros", read_only=True)
    cons = serializers.CharField(source="rating.cons", read_only=True)
    review = serializers.CharField(source="rating.review", read_only=True)
    rating = serializers.DecimalField(source="rating.rating", read_only=True, max_digits=2, decimal_places=1)

    meta_title = serializers.CharField(source="rating.meta_title", read_only=True)
    meta_description = serializers.CharField(
        source="rating.meta_description", read_only=True
    )
    user = UserSerializerList(source="rating.user", read_only=True)
    # Links to other external urls
    canonical_url = serializers.URLField(source="rating.canonical_url", read_only=True)
