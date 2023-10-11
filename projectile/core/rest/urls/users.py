from django.urls import path

from ..views.users import UserList

urlpatterns = [
    path(
        "/users", UserList.as_view(), name="user-list",
    ),
]
