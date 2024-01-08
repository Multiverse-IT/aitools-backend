from django.urls import path

from ..views import storage

urlpatterns = [
    path("", storage.PrivateCommonStorageList.as_view(), name="common-storage-list"),
    path("/<uuid:uid>", storage.PrivateCommonStorageDetail.as_view(), name="common-storage-detail")
]