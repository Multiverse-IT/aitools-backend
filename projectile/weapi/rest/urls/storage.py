from django.urls import path

from ..views import storage

urlpatterns = [
    path(
        "",
        storage.PrivateCommonStorageDetail.as_view(),
        name="common-storage-detail",
    )
]
