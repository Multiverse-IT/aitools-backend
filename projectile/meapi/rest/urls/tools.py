from django.urls import path

from ..views import tools

urlpatterns = [
    path("/love-tool", tools.UserLoveToolList.as_view(), name="love-tool"),
    path("/<slug:slug>", tools.PublicToolDetail.as_view(), name="tool-detail"),
    path(
        "/all/trending",
        tools.PublicTrendingToolList.as_view(),
        name="trending-tool-list",
    ),
    path(
        "/all/trending/<slug:slug>",
        tools.PublicTrendingToolDetail.as_view(),
        name="trending-tool-detail",
    ),
    path("/this/day", tools.PublicToolTodayList.as_view(), name="todays-tool"),
    path("", tools.PublicToolList.as_view(), name="tool-list"),
]
