from django.urls import path

from ..views import storage

urlpatterns = [
    path("", storage.PublicCommonStorageList.as_view(), name="common-storage-public-list"),
    path("/<uuid:uid>", storage.PublicCommonStorageDetail.as_view(), name="common-storage-public-detail")
]
