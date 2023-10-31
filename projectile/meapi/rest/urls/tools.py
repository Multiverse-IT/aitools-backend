from django.urls import path

from ..views import tools

urlpatterns = [
    path("", tools.PublicToolList.as_view(), name="tool-list"),
    path("/<slug:slug>", tools.PublicToolDetail.as_view(), name="tool-detail"),
]
