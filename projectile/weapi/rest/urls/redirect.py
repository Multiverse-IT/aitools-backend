from django.urls import path

from ..views import redirect

urlpatterns = [
    path("", redirect.PrivateRedirectList.as_view(), name="redirect-list"),
    path("/<uuid:uid>", redirect.PrivateRedirectDetail.as_view(), name="redirect-detail"),
]
