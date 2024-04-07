from rest_framework import generics

from contentio.models import FAQ
from contentio.rest.serializers.faq import GlobalFaqListSerializer

'''
Faq list and create
'''

class PrivateFaqList(generics.ListCreateAPIView):
    queryset = FAQ.objects.filter()
    serializer_class = GlobalFaqListSerializer
    permission_classes = []


class PrivateFaqDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FAQ.objects.filter()
    serializer_class = GlobalFaqListSerializer
    permission_classes = []
    lookup_field = "uid"