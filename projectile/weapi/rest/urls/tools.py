from django.urls import path

from ..views import tools

urlpatterns = [
    path(
        "/<slug:slug>/requested",
        tools.RequestToolResponseDetail.as_view(),
        name="accept-tool",
    ),
    path(
        "/verification/list",
        tools.PrivateCodeVerifyList.as_view(),
        name="verification-list",
    ),
    path(
        "/verification/list/<slug:slug>",
        tools.PrivateCodeVerifyDetail.as_view(),
        name="verification-detail",
    ),
    path("/top/hundred",
        tools.PrivateTopHundredToolsList.as_view(),
        name="top-hundred-tool-list"
    ),
    path("/top/hundred/<slug:slug>",
        tools.PrivateTopHundredToolsDetail.as_view(),
        name="top-hundred-tool-detail"
    ),
    path("/<slug:slug>", tools.ToolDetail.as_view(), name="my-tool-detail"),
    path("", tools.ToolList.as_view(), name="my-tool-list"),
]
