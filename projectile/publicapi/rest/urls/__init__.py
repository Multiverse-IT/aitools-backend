from django.urls import path, include

urlpatterns = [
    path("/tools", include("publicapi.rest.urls.tools")),
    path("/posts", include("publicapi.rest.urls.posts")),
    path("/sub-categories", include("publicapi.rest.urls.subcategory")),
]
