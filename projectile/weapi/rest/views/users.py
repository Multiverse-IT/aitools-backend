from core.choices import UserStatus
from core.models import User
from core.rest.serializers.users import UserSerializerList
from rest_framework import generics, permissions


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


class PrivateGoogleUserDetail(generics.ListAPIView):
    queryset = User.objects.filter(status=UserStatus.ACTIVE)
    serializer_class = UserSerializerList
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "slug"
