from django.urls import path

from ..views import me

urlpatterns = [
    path("", me.PrivateMeDetail.as_view(), name="me-detail"),
]
