from rest_framework import serializers

from authentication.models import AuthTokens


class AuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthTokens
        fields = "__all__"
