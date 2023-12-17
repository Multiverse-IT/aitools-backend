from django.urls import path

from ..views import subcategory

urlpatterns = [
    path("", subcategory.PublicApiSubCategoryList.as_view(), name="public-subcategory-api-list")
]