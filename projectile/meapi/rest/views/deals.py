from rest_framework import generics
from catalogio.models import Deal

from weapi.rest.serializers.deals import PrivateDealsSerializer


class PublicDealsList(generics.ListAPIView):
    queryset = Deal.objects.filter()
    serializer_class = PrivateDealsSerializer
    permission_classes = []

    def get_queryset(self):
        is_top = self.request.query_params.get("is_top", False)
        if is_top:
            queryset = self.queryset.filter(is_top=is_top)
            return queryset
        return self.queryset
