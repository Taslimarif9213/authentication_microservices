from rest_framework import serializers

from .utils import bcrypt_hash_password
from .models import Users


class RegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=255, required=True)
    last_name = serializers.CharField(max_length=255, required=True)
    email = serializers.CharField(max_length=255, required=True)
    mobile_no = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=255, required=True)

    def create(self, validated_data):
        user_data = {
            "first_name": validated_data["first_name"],
            "last_name": validated_data["last_name"],
            "email": validated_data["email"],
            "mobile_no": validated_data["mobile_no"],
            "password": bcrypt_hash_password(validated_data["password"]),
        }

        return Users.objects.create(**user_data)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["user_id", "first_name", "last_name", "email", "mobile_no"]


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["first_name", "last_name", "password", "mobile_no"]


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
