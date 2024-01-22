
from rest_framework import serializers

from ...models import Post

class PublicPostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "slug",
            "title",
            "avatar",
            "alt",
            "description",
            "short_description",
            "status",
            "meta_title",
            "meta_description",
            "canonical_url",
            "is_indexed",
            "focus_keyword",
            "created_at",
            "updated_at",
            "view_count"
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        return Post.objects.create(user=user, **validated_data)
