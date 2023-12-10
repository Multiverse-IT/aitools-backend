from django.urls import path

from ..views import feature_tool

urlpatterns = [
    path("", feature_tool.PublicFeatureToolList.as_view(), name="feature-tool-list"),
    path(
        "/<slug:slug>",
        feature_tool.PublicFeatureToolDetail.as_view(),
        name="feature-tool-detail",
    ),
]
