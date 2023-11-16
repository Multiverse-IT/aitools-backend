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
    first_name = serializers.CharField(max_length=50, write_only=True)
    iid = serializers.CharField(write_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = [
            "iid", 
            "id",
            "first_name",
            "name",
            "email",
            "image",
            "iat",
            "jti",
            "picture",
            "exp",
            "sub",
        ]
        read_only_fields = ["id"]

    def get_name(self, instance):
        return instance.first_name
    
    def create(self, validated_data):
        iid = validated_data.pop("iid")
        name = validated_data.pop("first_name")
        username = f"user_{iid}"

        try:
            user = User.objects.get(id=iid)
        except:
            validated_data["username"] = username
            validated_data["id"]=iid
            validated_data["first_name"] = name
            user = super().create(validated_data)

        return user
