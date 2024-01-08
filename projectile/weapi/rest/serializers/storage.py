from rest_framework import serializers

from contentio.models import CommonStorage

class PrivateCommonStorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonStorage
        fields = ["uid", "storage", "created_at", "updated_at"]
        read_only_fields = ["uid", "created_at", "updated_at"]

    def create(self, validated_data):
        common_storage = CommonStorage.objects.first()
        if common_storage:
            storage = validated_data.get("storage")
            common_storage.storage = storage
            common_storage.save()
        else:
            common_storage = CommonStorage.objects.create(**validated_data)
        return common_storage