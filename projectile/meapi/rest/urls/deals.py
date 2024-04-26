from django.urls import path

from ..views import deals

urlpatterns = [
    path("", deals.PublicDealsList.as_view(), name="deals-tool-list"),
]
