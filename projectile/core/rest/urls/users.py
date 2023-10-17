from django.urls import path

from ..views.login import GlobalLogin
from ..views.users import UserList

urlpatterns = [
    path(
        "/users",
        UserList.as_view(),
        name="user-list",
    ),
    path("/login", GlobalLogin.as_view(), name="global-login"),
]
