from rest_framework import serializers
from contentio.models import Redirect

class PrivateRedirectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Redirect
        fields = (
            "type",
            "is_permanent",
            "old",
            "new",
            "extras",
        )
