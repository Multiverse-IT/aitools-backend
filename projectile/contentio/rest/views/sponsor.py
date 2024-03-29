
from rest_framework import generics

from ...models import Sponsor
from ..serializers.sponsor import PublicSponsorListSerializer

'''
Sponsor list and create
'''

class PublicSponsorList(generics.CreateAPIView):
    serializer_class = PublicSponsorListSerializer
    permission_classes = []


class PublicSponsorDetail(generics.RetrieveUpdateAPIView):
    serializer_class = PublicSponsorListSerializer
    permission_classes = []

    def get_object(self):
        obj = Sponsor.objects.first()
        return obj
