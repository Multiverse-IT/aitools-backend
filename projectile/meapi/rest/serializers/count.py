from rest_framework import serializers

class PublicCountSerializer(serializers.Serializer):
    today_search_count = serializers.IntegerField()
    total_tools = serializers.IntegerField()
    today_created_tools = serializers.IntegerField()
    trending_tools = serializers.IntegerField()
    total_deals = serializers.IntegerField()

class PublicSubcategoryCountSerializer(serializers.Serializer):
    total_tools = serializers.IntegerField(read_only=True)
    today_created_tools = serializers.IntegerField(read_only=True)
    trending_tools = serializers.IntegerField(read_only=True)

