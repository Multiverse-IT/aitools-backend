from django.db.models import Q

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from core.models import User
from core.choices import UserStatus

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
    f_name = serializers.CharField(max_length=50, write_only=True)
    iid = serializers.CharField(write_only=True)
    e_mail = serializers.EmailField(write_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = [
            "iid",
            "id",
            "slug",
            "f_name",
            "e_mail",
            "name",
            "email",
            "image",
            "iat",
            "jti",
            "picture",
            "exp",
            "sub",
            "avatar",
            "created_at",
            "updated_at"
        ]
        read_only_fields = ["id", "email"]

    def get_name(self, instance):
        return instance.first_name

    def create(self, validated_data):
        iid = validated_data.pop("iid")
        e_mail = validated_data.pop("e_mail")
        name = validated_data.pop("f_name")
        username = f"user_{iid}"

        try:
            user = User.objects.get(id=int(iid))
        except:
            validated_data["username"] = username
            validated_data["id"]=iid
            validated_data["email"] = e_mail
            validated_data["first_name"] = name
            validated_data["status"] = UserStatus.ACTIVE
            user = super().create(validated_data)

        return user
       