from rest_framework import status
from rest_framework.views import APIView

from common.generic_response import GenericSuccessResponse
from core.constants.message import BAD_REQUEST, INVALID_PHONE_NUMBER, OTP_SENT_SUCCESSFULLY, USER_DOES_NOT_EXISTS
from users.utils import is_valid_mobile_number
from custom_security.authorization import PublicAPIPermission
from error_logging.db_log_handler import log_error
from exception_handler.generic_exception import GenericException, CustomBadRequest, CustomNotFound, BadRequest
from otp.models import OtpType
from otp.helpers import generate_otp
from otp.serializers import ValidateGenerateOTPSerializer
from users.models import Users

# Error-code: 1xxxx


class GenerateOTP(APIView):
    permission_classes = [PublicAPIPermission]

    @staticmethod
    def post(request):
        try:

            if not ValidateGenerateOTPSerializer(data=request.data).is_valid():
                return CustomBadRequest(message=BAD_REQUEST)

            if not is_valid_mobile_number(request.data["mobile_no"]):
                return CustomBadRequest(message=INVALID_PHONE_NUMBER)

            otp = generate_otp(request)

            if otp:
                return GenericSuccessResponse(
                    data={"otp": otp},
                    message=OTP_SENT_SUCCESSFULLY,
                    status=status.HTTP_201_CREATED)

        except Users.DoesNotExist as e:
            log_error(e, 10404)
            return CustomNotFound(message=USER_DOES_NOT_EXISTS)
        except BadRequest as e:
            raise BadRequest(e.detail)
        except Exception as e:
            log_error(e, 10000)
            return GenericException()


class OTPTypesView(APIView):
    permission_classes = [PublicAPIPermission]

    @staticmethod
    def get(request):
        try:
            otp_types = []
            for otp_type in OtpType:
                otp_types.append({
                    "key": otp_type.name,
                    "value": otp_type.value
                })

            return GenericSuccessResponse(data=otp_types, status=status.HTTP_200_OK)

        except Exception as e:
            log_error(e, 10000)
            return GenericException()
