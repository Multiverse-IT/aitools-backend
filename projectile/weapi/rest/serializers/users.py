from django.contrib.auth import get_user_model

User = get_user_model()

from rest_framework import serializers

class PrivateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "slug",
            "username",
            "email",
            "phone",
            "first_name",
            "last_name",
            "avatar",
            "description",
            "avatar",
            "status",
            "gender",
            "exp",
            "sub",
            "iat",
            "jti",
            "image",
            "picture",
            "date_of_birth",
            "created_at",
            "updated_at"
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
            "updated_at"
        ]