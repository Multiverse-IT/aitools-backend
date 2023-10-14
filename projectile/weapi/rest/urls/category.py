from django.urls import path

from ..views import category

urlpatterns = [
    path("", category.CatetoryList.as_view(), name="my-category-list"),
    path("/<slug:slug>", category.CategoryDetail.as_view(), name="my-category-detail"),
]
