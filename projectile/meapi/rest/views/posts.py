from contentio.choices import PostStatus
from contentio.models import Post
from contentio.rest.serializers.posts import PublicPostListSerializer
from rest_framework import generics


class PublicPostList(generics.ListAPIView):
    queryset = Post.objects.filter(status=PostStatus.ACTIVE)
    serializer_class = PublicPostListSerializer
    permission_classes = []

    def get_queryset(self):
        popular = self.request.query_params.get("popular", None)
        queryset = self.queryset

        if popular == "True":
            queryset = self.queryset.filter(view_count__gt=5).order_by("-view_count")[
                :5
            ]
        return queryset


class PublicPostDetail(generics.RetrieveAPIView):
    queryset = Post.objects.filter(status=PostStatus.ACTIVE)
    serializer_class = PublicPostListSerializer
    permission_classes = []

    def get_object(self):
        slug = self.kwargs.get("slug", None)
        post = generics.get_object_or_404(self.queryset.filter(), slug=slug)
        post.view_count += 1
        post.save()
        return post
