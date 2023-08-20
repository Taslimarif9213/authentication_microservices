from django.conf import settings

from twilio.rest import Client


from core.constants.message import USER_ACCOUNT_DELETED, USER_DOES_NOT_EXISTS, BAD_REQUEST
from error_logging.db_log_handler import log_error
from exception_handler.generic_exception import CustomBadRequest
from otp.models import OtpType
from otp.serializers import OTPSerializer
from otp.services import OTPService
from users.models import Users


def generate_otp(request):
    if request.data["otp_type"] == OtpType.LOGIN.value:
        user = Users.objects.filter(
            mobile_no=request.data["mobile_no"]).first()

        if user is not None:
            if user.is_deleted:
                raise CustomBadRequest(message=USER_ACCOUNT_DELETED)
           
        else:
            raise CustomBadRequest(message=USER_DOES_NOT_EXISTS)

    otp = OTPService().generate_otp()

    otp_serializer = OTPSerializer(data={
        "otp": otp,
        "otp_type": request.data["otp_type"],
        "mobile_no": request.data["mobile_no"],
    })
    
    if otp_serializer.is_valid():
        otp_serializer.save()

        mo_with_country_code = "+91" + str(request.data["mobile_no"])

        # Send OTP via Twilio SMS
        twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        twilio_from_number = settings.TWILIO_PHONE_NUMBER

        response = twilio_client.messages.create(
            body=f"Your Login OTP is: {otp}",
            from_=twilio_from_number,
            to=mo_with_country_code
        )
        request.session['otp'] = otp

        # Print the Twilio message SID for debugging
        print(response.sid)

        return otp
    else:
        log_error(BAD_REQUEST, 10400)
        raise CustomBadRequest(message=BAD_REQUEST)
