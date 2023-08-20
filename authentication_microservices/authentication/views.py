from django.db import transaction
from django.db.models import Q

from rest_framework import status
from rest_framework.views import APIView

from authentication.helpers import get_authentication_tokens, save_auth_tokens
from authentication.models import AuthTokens
from authentication.serializers import LogingWithPasswordSerializer
from core.constants.message import BAD_REQUEST, INVALID_PHONE_NUMBER, OTP_ALREADY_USED, OTP_EXPIRED, OTP_NOT_MATCHED, OTP_VERIFIED, USER_LOGGED_OUT, INVALID_PASSWORD
from common.generic_response import GenericSuccessResponse
from custom_security.authorization import PublicAPIPermission, JWTAuthentication
from error_logging.db_log_handler import log_error
from exception_handler.generic_exception import CustomBadRequest, BadRequest, GenericException, CustomNotFound
from otp.models import OTP
from otp.serializers import ValidateVerifyOTPSerializer
from otp.services import OTPService
from users.models import Users
from users.utils import validated_hashed_password


# Create your views here.


class Login(APIView):
    permission_classes = [PublicAPIPermission]

    @staticmethod
    def post(request):
        try:
            if not ValidateVerifyOTPSerializer(data=request.data).is_valid():
                return CustomBadRequest(message=BAD_REQUEST)

            if not Users.objects.filter(mobile_no=request.data["mobile_no"], is_deleted=False).exists():
                return CustomBadRequest(message=INVALID_PHONE_NUMBER)

            last_otp = OTP.objects.filter(mobile_no=request.data["mobile_no"],
                                          otp=request.data["otp"],
                                          otp_type=request.data["otp_type"]).last()
            if last_otp is None:
                log_error(OTP_NOT_MATCHED, 10410)
                return CustomBadRequest(message=OTP_NOT_MATCHED)

            elif last_otp.is_verified:
                return CustomBadRequest(message=OTP_ALREADY_USED)

            else:
                if OTPService().verify_otp(last_otp.created_at):
                    last_otp.is_verified = True
                    last_otp.save()

                    user = Users.objects.get(mobile_no=request.data["mobile_no"], is_deleted=False)

                    authentication_tokens = get_authentication_tokens(user)

                    save_auth_tokens(authentication_tokens)

                    return GenericSuccessResponse(data=authentication_tokens,
                                                  message=OTP_VERIFIED,
                                                  status=status.HTTP_200_OK)
                else:
                    return CustomBadRequest(message=OTP_EXPIRED)

        except BadRequest as e:
            raise BadRequest(e.detail)
        except Exception as e:
            log_error(e, 10000)
            return GenericException()
        

class LogingWithPassword(APIView):
    permission_classes = [PublicAPIPermission]

    @staticmethod
    def post(request):
        try:
            if not LogingWithPasswordSerializer(data=request.data).is_valid():
                return CustomBadRequest(message=BAD_REQUEST)
            
            user = Users.objects.get(mobile_no=request.data["mobile_no"], is_deleted=False)
            
            if user is None:
                raise CustomBadRequest(message=INVALID_PHONE_NUMBER)
            

            if validated_hashed_password(request.data["password"], user.password):
                authentication_tokens = get_authentication_tokens(user)

                save_auth_tokens(authentication_tokens)

                return GenericSuccessResponse(data=authentication_tokens,
                                              status=status.HTTP_200_OK)
            else:
                return CustomBadRequest(message=INVALID_PASSWORD)
            

        except Users.DoesNotExist as e:
            log_error(e, 10404)
            return CustomNotFound(message=INVALID_PHONE_NUMBER)
        except BadRequest as e:
            raise BadRequest(e.detail)
        except Exception as e:
            log_error(e, 10000)
            return GenericException()


class Logout(APIView):
    authentication_classes = [JWTAuthentication]

    @staticmethod
    def post(request):
        try:
            with transaction.atomic():
                token = request.headers.get("authorization").split(" ")[1]

                AuthTokens.objects.filter(Q(access_token=token) | Q(refresh_token=token)).delete()

                return GenericSuccessResponse(message=USER_LOGGED_OUT,
                                              status=status.HTTP_200_OK)

        except Exception as e:
            log_error(e, 14000)
            return GenericException()
