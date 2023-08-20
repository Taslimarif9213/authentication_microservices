from rest_framework import serializers

from otp.models import OTP


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = "__all__"
        

class ValidateGenerateOTPSerializer(serializers.Serializer):
    mobile_no = serializers.CharField(max_length=255, required=True)
    otp_type = serializers.CharField(max_length=255, required=True)

    def validate(self, attrs):
        return attrs


class ValidateVerifyOTPSerializer(serializers.Serializer):
    mobile_no = serializers.CharField(max_length=255, required=True)
    otp = serializers.IntegerField(required=True)
    otp_type = serializers.CharField(max_length=255, required=True)
    
    def validate(self, attrs):
        return attrs
