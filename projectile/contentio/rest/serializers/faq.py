from rest_framework import serializers

from ...models import FAQ


class GlobalFaqListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = [
           "uid",
           "title",
           "slug",
           "summary",
           "priority",
           "created_at",
           "updated_at",
        ]


class GlobalFaqListSlimSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='faq.title', read_only=True)
    uid = serializers.CharField(source="faq.uid", read_only=True)
    slug = serializers.CharField(source='faq.slug', read_only=True)
    summary = serializers.CharField(source="faq.summary", read_only=True)
    priority = serializers.CharField(source='faq.priority', read_only=True)
    created_at = serializers.DateTimeField(source="faq.created_at", read_only=True)
    class Meta:
        model = FAQ
        fields = [
           "uid",
           "title",
           "slug",
           "summary",
           "priority",
           "created_at",
           "updated_at",
        ]
