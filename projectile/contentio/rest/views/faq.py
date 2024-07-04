
from rest_framework import generics

from ...models import FAQ
from ..serializers.faq import GlobalFaqListSerializer

'''
Sponsor list and create
'''

class GlobalFaqList(generics.ListAPIView):
    queryset = FAQ.objects.filter()
    serializer_class = GlobalFaqListSerializer
    permission_classes = []

    def get_queryset(self):
        queryset = self.queryset
        sub_category_slug = self.request.query_params.get("sub_category_slug", None)
        if sub_category_slug is not None:
            queryset = queryset.filter(
                faqcategoryconnector__sub_category__slug=sub_category_slug
            )
        return queryset


class GlobalFaqDetail(generics.RetrieveAPIView):
    queryset = FAQ.objects.filter()
    serializer_class = GlobalFaqListSerializer
    permission_classes = []
    lookup_field = "slug"