
from rest_framework import serializers

from ...models import Sponsor

class PublicSponsorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = [
            "uid",
            "name",
            "link",
            "description",
            "created_at",
            "updated_at",
        ]