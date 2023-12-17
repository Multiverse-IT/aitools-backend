
from rest_framework import serializers

from catalogio.models import SubCategory
from common.serializers import CategorySlimSerializer


class PublicApiSubCatetoryListDetailSerializer(serializers.ModelSerializer):
    category = CategorySlimSerializer(
        source="toolscategoryconnector_set.first", read_only=True
    )

    class Meta:
        model = SubCategory
        fields = [
            "slug",
            "title",
            "category",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields