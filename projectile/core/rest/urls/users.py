from django.urls import path

from ..views.login import GlobalLogin, GlobalRegister
from ..views.users import UserList, GoogleUserList

urlpatterns = [
    path(
        "/users",
        UserList.as_view(),
        name="user-list",
    ),
    path("/google/users", GoogleUserList.as_view(), name="google-user-list"),
    path("/login", GlobalLogin.as_view(), name="global-login"),
    path("/register", GlobalRegister.as_view(), name="global-register"),
]
