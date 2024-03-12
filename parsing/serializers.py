from rest_framework import serializers

class UrlSerializer(serializers.Serializer):
    URL = serializers.URLField()
 