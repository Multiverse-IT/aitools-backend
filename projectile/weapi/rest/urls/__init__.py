from django.urls import path, include

from ..views import tools

urlpatterns = [
    path("/tools", include("weapi.rest.urls.tools")),
    path("/categories", include("weapi.rest.urls.category")),
    path("/sub-categories", include("weapi.rest.urls.sub_category")),
    path("/features", include("weapi.rest.urls.feature")),
    path("/ratings", include("weapi.rest.urls.rating")),
    path("/google", include("weapi.rest.urls.users")),
]
