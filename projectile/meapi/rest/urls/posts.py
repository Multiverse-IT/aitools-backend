from django.urls import path

from ..views import posts

urlpatterns = [
    path("", posts.PublicPostList.as_view(), name="public-post-list"),
    path("/<slug:slug>", posts.PublicPostDetail.as_view(), name="public-post-detail"),
]
