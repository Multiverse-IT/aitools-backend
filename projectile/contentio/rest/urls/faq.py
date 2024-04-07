
from django.urls import path

from ..views.faq import GlobalFaqDetail, GlobalFaqList

urlpatterns = [
    path("/<slug:slug>", GlobalFaqDetail.as_view(), name="faq-detail"),
    path("", GlobalFaqList.as_view(), name="faq-list"),
]