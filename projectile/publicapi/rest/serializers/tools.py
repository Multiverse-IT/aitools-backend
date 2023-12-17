
from rest_framework import serializers

from catalogio.models import (
    Tool
)


class PublicApiToolListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = [
            "slug",
            "name",
            "created_at",
        ]
        read_only_fields = fields