from django.urls import path, include

urlpatterns = [
    path(r"/users", include("core.rest.urls.users")),
]
