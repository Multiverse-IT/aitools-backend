from django.urls import path

from ..views import count

urlpatterns = [
    path("", count.CountOfEveryThingList.as_view(), name="all-counts"),
]
