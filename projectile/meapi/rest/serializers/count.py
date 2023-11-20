from rest_framework import serializers

class PublicCountSerializer(serializers.Serializer):
    today_search_count = serializers.IntegerField()
    total_tools = serializers.IntegerField()
    today_created_tools = serializers.IntegerField()
    trending_tools = serializers.IntegerField()
