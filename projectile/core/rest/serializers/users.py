
from rest_framework import serializers
from ...models import User

class UserSerializerList(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "uid",
            "slug",
            "username",
            "email",
            "phone",
            "first_name",
            "last_name",
            "description",
            "avatar",
            "status",
            "gender",
            "exp",
            "sub",
            "iat",
            "jti",
            "date_of_birth",
            "created_at",
            "updated_at"
        ]
        read_only_fields = ["__all__"]
