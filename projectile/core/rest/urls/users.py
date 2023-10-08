from django.urls import path

from ..views.users import UserList

urlpatterns = [
    path(
        "", UserList.as_view(), name="user-list",
    ),
]
