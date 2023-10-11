from django.urls import path, include

from ..views import tools

urlpatterns = [
    path("/tools", include("weapi.rest.urls.tools"))
]
