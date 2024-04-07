
from django.urls import path

from ..views.faq import PrivateFaqDetail, PrivateFaqList

urlpatterns = [
    path("/<uuid:uid>", PrivateFaqDetail.as_view(), name="private-faq-detail"),
    path("", PrivateFaqList.as_view(), name="private-faq-list"),
]