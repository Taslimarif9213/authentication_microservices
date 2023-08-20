from enum import Enum

from django.db import models



class OtpType(Enum):
    LOGIN = "LOGIN"

    @classmethod
    def choices(cls):
        return [(otp_type.name, otp_type.value) for otp_type in cls]


class OTP(models.Model):
    class Meta:
        db_table = 'ins_otp'

    otp_type = models.CharField(max_length=255, choices=OtpType.choices(), db_column='otp_type')
    otp = models.IntegerField(db_column='otp_code')
    expiry = models.IntegerField(default=120, db_column='otp_expiry')
    mobile_no = models.CharField(max_length=50, db_column='otp_mobile_number')
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    