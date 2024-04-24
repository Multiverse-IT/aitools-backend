from rest_framework import serializers

from ...models import FAQ

class GlobalFaqListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = [
           "uid",
           "title",
           "slug",
           "summary",
           "priority",
           "created_at",
           "updated_at",
        ]