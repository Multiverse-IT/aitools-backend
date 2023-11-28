from rest_framework import generics

from ...choices import PostStatus
from ...models import Post
from ..serializers.posts import PublicPostListSerializer


class PublicPostList(generics.ListCreateAPIView):
    queryset = Post.objects.filter(status=PostStatus.ACTIVE)
    serializer_class = PublicPostListSerializer
    permission_classes = []


class PublicPostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.filter(status=PostStatus.ACTIVE)
    serializer_class = PublicPostListSerializer
    permission_classes = []
    lookup_field = "slug"
