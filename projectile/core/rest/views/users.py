from rest_framework import generics, permissions

from ...models import User
from ..serializers.users import UserSerializerList


class UserList(generics.ListAPIView):
    queryset = User.objects.filter()
    serializer_class = UserSerializerList
    permission_classes = [permissions.IsAdminUser]


# class UserList(generics.ListAPIView):
#     queryset = User.objects.filter(exp__isnull=True, iat__isnull=True, sub__isnull=True, jti__isnull=True)
#     serializer_class = UserSerializerList
#     permission_classes = [permissions.IsAdminUser]

    