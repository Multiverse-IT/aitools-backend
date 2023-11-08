from django.db.models import Q

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from core.models import User
from core.utils import get_tokens_for_user

from .users import UserSerializerList

class PublicUserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=255,
        help_text="You can login by phone number or email",
        write_only=True,
    )
    # password = serializers.CharField(min_length=5, max_length=50, write_only=True)
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)
    user = UserSerializerList(read_only=True)

    def create(self, validated_data):
        username = validated_data.get("username")
        # password = validated_data.get("password")
        try:
            user: User = User.objects.get(
                Q(email=username)
                | Q(phone=username)
                | Q(username=username)
            )
            # if not user.check_password(password):
            #     raise AuthenticationFailed()

            token = get_tokens_for_user(user)
            validated_data["refresh"] = token["refresh"]
            validated_data["access"] = token["access"]
            validated_data["user"]  = user

            return validated_data

        except User.DoesNotExist:
            raise AuthenticationFailed()
        

class PublicUserRegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50, required=False)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "image",
            "iid", 
            "exp",
            "sub",
        ]

