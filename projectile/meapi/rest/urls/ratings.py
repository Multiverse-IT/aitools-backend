from django.urls import path

from ..views import ratings

urlpatterns = [
    path("", ratings.RatingList.as_view(), name="rating-list"),
    path("/<uuid:uid>", ratings.RatingDetail.as_view(), name="rating-detail"),
]
