from catalogio.models import Feature
from rest_framework import serializers


class FeatureListDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = [
            "slug",
            "title",
            "meta_title",
            "meta_description",
            "canonical_url",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
