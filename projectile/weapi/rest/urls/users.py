from django.urls import path

from ..views import users

urlpatterns = [
    path("/users", users.PrivateGoogleUserList.as_view(), name="google-user-list"),
    path(
        "/users/<slug:slug>",
        users.PrivateGoogleUserDetail.as_view(),
        name="google-user-detail",
    ),
]
