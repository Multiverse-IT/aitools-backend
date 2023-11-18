from rest_framework import generics, permissions

from core.choices import UserStatus

from ...models import User
from ..serializers.users import UserSerializerList

class UserList(generics.ListAPIView):
    queryset = User.objects.filter()
    serializer_class = UserSerializerList
    permission_classes = [permissions.IsAdminUser]


class GoogleUserList(generics.ListAPIView):
    queryset = User.objects.filter()
    serializer_class = UserSerializerList
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return self.queryset.filter(
            exp="",
            iat="",
            sub="",
            jti="",
            status = UserStatus.ACTIVE
        )
