from django.urls import path

from ..views.feature_tool import PrivateFeatureToolDetail, PrivateFeatureToolList

urlpatterns = [
    path("", PrivateFeatureToolList.as_view(), name="feature-tool-list"),
    path(
        "/<slug:slug>", PrivateFeatureToolDetail.as_view(), name="feature-tool-detail"
    ),
]
