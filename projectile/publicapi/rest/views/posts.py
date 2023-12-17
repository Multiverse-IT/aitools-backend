from rest_framework import generics

from contentio.models import Post

from ..serializers.posts import PublicPostListSerializer


class PublicApiPostList(generics.ListAPIView):
    queryset = Post.objects.get_status_active()
    serializer_class = PublicPostListSerializer
    permission_classes = []
    pagination_class = None

