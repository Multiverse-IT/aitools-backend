from django.urls import path, include

from ..views import tools

urlpatterns = [
    path("/tools", include("weapi.rest.urls.tools")),
    path("/categories", include("weapi.rest.urls.category")),
    path("/sub-categories", include("weapi.rest.urls.sub_category")),

]
