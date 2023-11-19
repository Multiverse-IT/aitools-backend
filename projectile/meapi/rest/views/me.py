from core.rest.serializers.users import UserSerializerList
from rest_framework.generics import RetrieveUpdateAPIView


class PrivateMeDetail(RetrieveUpdateAPIView):
    serializer_class = UserSerializerList

    def get_object(self):
        return self.request.user
