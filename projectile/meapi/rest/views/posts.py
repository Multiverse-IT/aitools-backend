
from contentio.models import Post
from rest_framework import generics
from contentio.choices import PostStatus
from contentio.rest.serializers.posts import PublicPostListSerializer

class PublicPostList(generics.ListAPIView):
    queryset = Post.objects.filter(status=PostStatus.ACTIVE)
    serializer_class = PublicPostListSerializer
    permission_classes = []


class PublicPostDetail(generics.RetrieveAPIView):
    queryset = Post.objects.filter(status=PostStatus.ACTIVE)
    serializer_class = PublicPostListSerializer
    permission_classes = []
    lookup_field = "slug"
