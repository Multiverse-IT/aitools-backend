from rest_framework import generics, permissions
from rest_framework.generics import get_object_or_404

from core.choices import UserStatus
from core.models import User
from core.permissions import IsAdmin
from core.rest.serializers.users import UserSerializerList
from ..serializers.users import PrivateUserSerializer

class PrivateGoogleUserList(generics.ListAPIView):
    queryset = User.objects.filter()
    serializer_class = UserSerializerList
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        print("sef:", self.queryset)
        return self.queryset.filter(status=UserStatus.ACTIVE).exclude(
            exp="",
            iat="",
            sub="",
            jti="",
        )

class PrivateGoogleUserDetail(generics.RetrieveAPIView):
    queryset = User.objects.filter(status=UserStatus.ACTIVE)
    serializer_class = UserSerializerList
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "slug"


class PrivateUserList(generics.ListCreateAPIView):
    queryset = User.objects.filter()
    serializer_class = PrivateUserSerializer
    permission_classes = [IsAdmin]
    
class PrivateUserDetail(generics.RetrieveDestroyAPIView):
    queryset = User.objects.filter()
    serializer_class = PrivateUserSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'slug'
    
