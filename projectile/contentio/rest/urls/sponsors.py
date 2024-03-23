
from django.urls import path

from ..views.sponsor import PublicSponsorList

urlpatterns = [
    path("", PublicSponsorList.as_view(), name="sponsors-list"),
]