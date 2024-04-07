
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


class GlobalFaqDetail(generics.RetrieveAPIView):
    queryset = FAQ.objects.filter()
    serializer_class = GlobalFaqListSerializer
    permission_classes = []
    lookup_field = "slug"