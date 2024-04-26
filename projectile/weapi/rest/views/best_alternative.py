from rest_framework import generics
from catalogio.models import BestAlternativeTool
from core.permissions import IsAdmin

from ..serializers.feature_tool import PrivateBestAlternativeToolSerializer

class PrivateBestAlternativeToolList(generics.ListCreateAPIView):
    queryset = BestAlternativeTool.objects.filter()
    serializer_class = PrivateBestAlternativeToolSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        from rest_framework import status
        from rest_framework.response import Response

        category_slug = self.kwargs.get('category_slug', None)
        if category_slug is None:
            return Response({"detail": "Category slug is missing"}, status=status.HTTP_404_NOT_FOUND)

        return self.queryset.filter(category__slug = category_slug)



class PrivateBestAlternativeToolDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BestAlternativeTool.objects.filter()
    serializer_class = PrivateBestAlternativeToolSerializer
    permission_classes = [IsAdmin]
    lookup_field = "slug"

    def get_object(self):
        from rest_framework.generics import get_object_or_404

        category_slug = self.kwargs.get('category_slug', None)
        slug = self.kwargs.get("slug", None)

        best_al_tool = get_object_or_404(self.queryset, category__slug=category_slug, slug=slug)

        return best_al_tool
