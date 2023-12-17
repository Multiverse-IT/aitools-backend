from django.urls import path

from ..views import tools
from ..views.count import PublicSubcategoryToolsCountList
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
    path(
        "/subcategory/<slug:subcategory_slug>",
        tools.PublicSubCategoryToolList.as_view(),
        name="subcategory-tool-list",
    ),
    path(
        "/subcategory/<slug:subcategory_slug>/counts",
        PublicSubcategoryToolsCountList.as_view(),
        name="subcategory-tool-counts",
    ),
    path("", tools.PublicToolList.as_view(), name="tool-list"),
]
