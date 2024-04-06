from rest_framework import generics
from catalogio.models import BestAlternativeTool
from core.permissions import IsAdmin

from ..serializers.feature_tool import PrivateBestAlternativeToolSerializer

class PrivateBestAlternativeToolList(generics.ListCreateAPIView):
    queryset = BestAlternativeTool.objects.filter()
    serializer_class = PrivateBestAlternativeToolSerializer
    permission_classes = [IsAdmin]


class PrivateBestAlternativeToolDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BestAlternativeTool.objects.filter()
    serializer_class = PrivateBestAlternativeToolSerializer
    permission_classes = [IsAdmin]
    lookup_field = "uid"
