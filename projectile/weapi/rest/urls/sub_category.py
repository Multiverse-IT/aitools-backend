from django.urls import path

from ..views import category

urlpatterns = [
    path(
        "",
        category.SubCategoryListWithCategoryTitle.as_view(),
        name="sub-categories",
    ),
]
