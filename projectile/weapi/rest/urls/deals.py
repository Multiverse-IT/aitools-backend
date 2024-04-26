from django.urls import path

from ..views.deals import PrivateDealsList

urlpatterns = [
    path("", PrivateDealsList.as_view(), name="deals-list"),
]
