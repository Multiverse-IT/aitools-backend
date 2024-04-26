from rest_framework import generics
from catalogio.models import Deal
from core.permissions import IsAdmin

from ..serializers.deals import PrivateDealsSerializer


class PrivateDealsList(generics.ListCreateAPIView):
    queryset = Deal.objects.filter()
    serializer_class = PrivateDealsSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        is_top = self.request.query_params.get("is_top", False)
        if is_top:
            queryset = self.queryset.filter(is_top=is_top)
            return queryset
        return self.queryset
