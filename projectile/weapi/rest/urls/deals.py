from django.urls import path

from ..views.deals import PrivateDealsList, PrivateDealsDetail

urlpatterns = [
    path("", PrivateDealsList.as_view(), name="deals-list"),
    path("/<slug:slug>", PrivateDealsDetail.as_view(), name="deal-detail"),
]
