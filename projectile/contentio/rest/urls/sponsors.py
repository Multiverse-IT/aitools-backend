
from django.urls import path

from ..views.sponsor import PublicSponsorList, PublicSponsorDetail

urlpatterns = [
    path("", PublicSponsorList.as_view(), name="sponsors-list"),
    path("/<uuid:uid>", PublicSponsorDetail.as_view(), name="sponor-detail")
]