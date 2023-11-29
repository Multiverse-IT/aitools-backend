
from rest_framework import serializers

from ...models import Post

class PublicPostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "slug",
            "title",
            "avatar",
            "description",
            "status",
            "created_at", 
            "updated_at",
        ]