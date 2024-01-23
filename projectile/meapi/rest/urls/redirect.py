from django.urls import path

from ..views import redirect

urlpatterns = [
    path("", redirect.PublicRedirectList.as_view(), name="public-redirect-list"),
    path(
        "/<uuid:uid>",
        redirect.PublicRedirectDetail.as_view(),
        name="public-redirect-detail",
    ),
]
