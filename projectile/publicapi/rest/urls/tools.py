from django.urls import path

from ..views import tools

urlpatterns = [
    path("", tools.PublicApiToolList.as_view(), name="public-tool-api-list")
]