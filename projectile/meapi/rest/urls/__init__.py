from django.urls import path, include

from ..views import tools

urlpatterns = [
    path("/tools", include("meapi.rest.urls.tools")),
    path("/ratings", include("meapi.rest.urls.ratings")),
    path("", include("meapi.rest.urls.me")),
]
