from rest_framework import generics

from ...models import Post
from ..serializers.posts import PublicPostListSerializer
from core.permissions import IsAdmin

class PublicPostList(generics.ListCreateAPIView):
    queryset = Post.objects.get_status_editable()
    serializer_class = PublicPostListSerializer
    permission_classes = [IsAdmin]


class PublicPostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.get_status_editable()
    serializer_class = PublicPostListSerializer
    permission_classes = [IsAdmin]

    def get_object(self):
        slug = self.kwargs.get("slug", None)
        post = generics.get_object_or_404(self.queryset.filter(), slug=slug)
        post.view_count += 1
        post.save()
        return post
