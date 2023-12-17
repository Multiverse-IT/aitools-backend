from rest_framework import generics

from catalogio.models import SubCategory

from ..serializers.subcategory import PublicApiSubCatetoryListDetailSerializer


class PublicApiSubCategoryList(generics.ListAPIView):
    serializer_class = PublicApiSubCatetoryListDetailSerializer
    permission_classes = []
    pagination_class = None

    def get_queryset(self):
        return SubCategory.objects.filter()
