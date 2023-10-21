from django.urls import path

from ..views import rating

urlpatterns = [
    path("", rating.RatingList.as_view(), name="my-rating-list"),
    path("/<slug:slug>", rating.RatingDetail.as_view(), name="my-rating-detail"),
]
