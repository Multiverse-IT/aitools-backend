from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from catalogio.models import Category, SubCategory

from ..serializers.category import (
    CatetoryListSerializer,
    SubCatetoryListByCategorySerializer,
)


class CatetoryList(generics.ListAPIView):
    queryset = Category.objects.filter()
    serializer_class = CatetoryListSerializer
    permission_classes = []

    def get_queryset(self):
        return self.queryset


class SubCategoryList(generics.ListAPIView):
    queryset = SubCategory.objects.filter()
    serializer_class = SubCatetoryListByCategorySerializer

    def get_queryset(self):
        slug = self.kwargs.get("slug", None)
        return self.queryset.filter(category__slug=slug)


class SubCategoryListWithCategoryTitle(APIView):
    def get(self, request):
        subcategory_dict = {}
        queryset = SubCategory.objects.filter()

        for sub_category in queryset:
            category = sub_category.category.title
            sub_category_data = SubCatetoryListByCategorySerializer(sub_category).data
            if category not in subcategory_dict:
                subcategory_dict[category] = []
            subcategory_dict[category].append(sub_category_data)

        subcategory_list = [
            {"category": category, "sub_category": sub_category}
            for category, sub_category in subcategory_dict.items()
        ]

        return Response(subcategory_list, status=status.HTTP_200_OK)
