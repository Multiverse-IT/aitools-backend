from django.urls import path

from ..views import tools

urlpatterns = [
    path("", tools.ToolList.as_view(), name="my-tool-list"),
    path("/<slug:slug>", tools.ToolDetail.as_view(), name="my-tool-detail"),
]
