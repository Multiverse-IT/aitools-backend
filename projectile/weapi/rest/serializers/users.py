from django.contrib.auth import get_user_model

from rest_framework import serializers

from core.choices import UserRole, UserStatus

User = get_user_model()


class PrivateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "slug",
            "email",
            "phone",
            "first_name",
            "last_name",
            "avatar",
            "description",
            "status",
            "gender",
            "password",
            "exp",
            "sub",
            "iat",
            "jti",
            "image",
            "picture",
            "date_of_birth",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "description",
            "avatar",
            "status",
            "exp",
            "sub",
            "iat",
            "jti",
            "image",
            "picture",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        email = validated_data.get("email").lower()
        user = User.objects.create(
            username=email,
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE,
            **validated_data
        )
        user.set_password(password)
        user.save()
        return user
