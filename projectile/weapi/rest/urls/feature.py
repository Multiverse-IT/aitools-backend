from django.urls import path

from ..views import feature

urlpatterns = [
    path("", feature.FeatureList.as_view(), name="my-feature-list"),
    path("/<slug:slug>", feature.FeatureDetail.as_view(), name="my-feature-detail"),
]
