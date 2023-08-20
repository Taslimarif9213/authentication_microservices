from rest_framework import serializers

from authentication.models import AuthTokens


class AuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthTokens
        fields = "__all__"


class LogingWithPasswordSerializer(serializers.Serializer):
    mobile_no = serializers.CharField(max_length=10, required=True)
    password = serializers.CharField(max_length=255, required=True)

    def validate(self, attrs):
        return attrs
