from rest_framework import serializers

from contentio.models import CommonStorage

class PrivateCommonStorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonStorage
        fields = ["uid", "storage", "created_at", "updated_at"]
        read_only_fields = ["uid", "created_at", "updated_at"]