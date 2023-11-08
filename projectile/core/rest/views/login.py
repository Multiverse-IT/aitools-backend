from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..serializers.login import PublicUserLoginSerializer, PublicUserRegisterSerializer


class GlobalLogin(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PublicUserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = super().create(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK, data=data.data)
    

class GlobalRegister(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PublicUserRegisterSerializer

    def post(self, request, *args, **kwargs):
        data = super().create(request, *args, **kwargs)
        return Response(status=status.HTTP_201_CREATED, data=data.data)
    