from django.urls import path

from ..views import users

urlpatterns = [
    path("", users.PrivateUserList.as_view(), name="user-list"),
    
]