from rest_framework import generics, permissions

from ...models import User
from ..serializers.users import UserSerializerList


class UserList(generics.ListAPIView):
    queryset = User.objects.filter()
    serializer_class = UserSerializerList
    permission_classes = [permissions.IsAdminUser]
