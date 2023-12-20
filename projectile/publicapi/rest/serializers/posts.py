
from rest_framework import serializers

from contentio.models import Post

class PublicApiPostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "slug",
            "title",
            "created_at", 
            "updated_at",
        ]
    
        read_only_fields = fields
