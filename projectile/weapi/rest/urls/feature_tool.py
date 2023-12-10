from django.urls import path

from ..views.feature_tool import PrivateFeatureToolList

urlpatterns = [ 
    path("", PrivateFeatureToolList.as_view(), name="feature-tool-list"),
]