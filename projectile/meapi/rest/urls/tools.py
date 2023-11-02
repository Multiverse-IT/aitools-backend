from django.urls import path

from ..views import tools

urlpatterns = [
    path("/love-tool", tools.UserLoveToolList.as_view(), name="love-tool"),
    path("/<slug:slug>", tools.PublicToolDetail.as_view(), name="tool-detail"),
    path("", tools.PublicToolList.as_view(), name="tool-list"),
]
