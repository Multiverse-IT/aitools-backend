from django.urls import path

from ..views import tools
from ..views.count import PublicSubcategoryToolsCountList

urlpatterns = [
    path("/love-tool", tools.UserLoveToolList.as_view(), name="love-tool"),
    path("/<slug:slug>", tools.PublicToolDetail.as_view(), name="tool-detail"),
    path("/<slug:slug>/verify", tools.PublicCodeVerifyApi.as_view(), name="verify-api"),
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
    path("/subcategory/<slug:subcategory_slug>/extra-fields",
        tools.PublicSubCategoryToolListExtraField.as_view(),
        name="subcategory-extra-fields"
    ),
    path(
        "/subcategory/<slug:subcategory_slug>/counts",
        PublicSubcategoryToolsCountList.as_view(),
        name="subcategory-tool-counts",
    ),
    path("/new/random",
        tools.PublicRandomSearch.as_view(),
        name = "new-search-api"
    ),
    path("/suggession/list",
        tools.PublicSuggessionList.as_view(),
        name="suggession-list-api"
        ),
    # path("/top/hundred",
    #     tools.PublicTopHundredToolsList.as_view(),
    #     name="public-top-hundred-tool-list"
    # ),
    # path("/top/hundred/<slug:slug>",
    #     tools.PublicTopHundredToolsDetail.as_view(),
    #     name="public-top-hundred-tool-detail"
    # ),
    path("/best/alternative",
        tools.PublicBestAlternativeToolList.as_view(),
        name="public-best-tool-list",
    ),
    path("/best/alternative/<slug:slug>",
        tools.PublicBestAlternativeToolDetail.as_view(),
        name="public-best-tool-detail",
    ),
    path("", tools.PublicToolList.as_view(), name="tool-list"),
]
