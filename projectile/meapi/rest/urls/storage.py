from django.urls import path

from ..views import storage

urlpatterns = [
    path("", storage.PublicCommonStorageList.as_view(), name="common-storage-public-list"),
]
