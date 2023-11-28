
from django.urls import path

from ..views.posts import PublicPostList, PublicPostDetail

urlpatterns = [ 
    path("", PublicPostList.as_view(), name="post-list"),
    path("/<slug:slug>", PublicPostDetail.as_view(), name="post-detail"),
]