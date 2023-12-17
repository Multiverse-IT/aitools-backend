from django.urls import path

from ..views import posts

urlpatterns = [
    path("", posts.PublicApiPostList.as_view(), name="public-post-api-list")
]