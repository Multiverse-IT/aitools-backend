from django.urls import path

from ..views import category

urlpatterns = [
    path(
        "",
        category.SubCategoryList.as_view(),
        name="sub-categories-list",
    ),
    path(
        "/<slug:slug>",
        category.
        SubcategoryDetail.as_view(),
        name="sub-categories",
    ),
    path(
        "/value/example",
        category.SubCategoryListWithCategoryTitle.as_view(),
        name="sub-categories",
    ),
]
