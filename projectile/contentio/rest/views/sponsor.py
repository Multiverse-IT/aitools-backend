
from rest_framework import generics

from ...models import Sponsor
from ..serializers.sponsor import PublicSponsorListSerializer

'''
Sponsor list and create
'''

class PublicSponsorList(generics.ListCreateAPIView):
    serializer_class = PublicSponsorListSerializer
    permission_classes = []

    def get_queryset(self):
        return Sponsor.objects.filter()

class PublicSponsorDetail(generics.RetrieveUpdateAPIView):
    serializer_class = PublicSponsorListSerializer
    permission_classes = []
    lookup_field = "uid"

    def get_queryset(self):
        return Sponsor.objects.filter()