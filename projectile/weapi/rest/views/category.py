from catalogio.models import Category, SubCategory
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.category import (
    CatetoryListSerializer,
    SubCatetoryListDetailSerializer,
)


class CatetoryList(generics.ListCreateAPIView):
    queryset = Category.objects.filter()
    serializer_class = CatetoryListSerializer
    permission_classes = []

    def get_queryset(self):
        return self.queryset


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.filter()
    serializer_class = CatetoryListSerializer
    permission_classes = []
    lookup_field = "slug"


class SubCategoryList(generics.ListCreateAPIView):
    serializer_class = SubCatetoryListDetailSerializer
    permission_classes = []

    def get_queryset(self):
        return SubCategory.objects.filter()


class SubcategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubCategory.objects.filter()
    serializer_class = SubCatetoryListDetailSerializer
    lookup_field = "slug"
    permission_classes = []


class SubCategoryListWithCategoryTitle(APIView):
    permission_classes = []

    def get(self, request):
        subcategory_dict = {}
        queryset = SubCategory.objects.filter()

        for sub_category in queryset:
            category = sub_category.category.title
            sub_category_data = SubCatetoryListDetailSerializer(sub_category).data
            if category not in subcategory_dict:
                subcategory_dict[category] = []
            subcategory_dict[category].append(sub_category_data)

        subcategory_list = [
            {"category": category, "sub_category": sub_category}
            for category, sub_category in subcategory_dict.items()
        ]

        return Response(subcategory_list, status=status.HTTP_200_OK)
