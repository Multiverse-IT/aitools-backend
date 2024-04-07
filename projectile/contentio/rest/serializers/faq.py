from rest_framework import serializers

from ...models import FAQ

class GlobalFaqListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = [
           "uid",
           "title",
           "slug",
           "image",
           "summary",
           "priority",
           "created_at",
           "updated_at",
        ]