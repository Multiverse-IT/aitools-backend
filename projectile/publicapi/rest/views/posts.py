from rest_framework import generics

from contentio.models import Post

from ..serializers.posts import PublicApiPostListSerializer


class PublicApiPostList(generics.ListAPIView):
    queryset = Post.objects.get_status_active()
    serializer_class = PublicApiPostListSerializer
    permission_classes = []
    pagination_class = None

