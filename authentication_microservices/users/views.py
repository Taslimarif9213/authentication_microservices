from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from rest_framework import status
from rest_framework.views import APIView

from authentication.helpers import get_authentication_tokens, save_auth_tokens
from common.generic_response import GenericSuccessResponse
from core.settings.base import EMAIL_HOST
from core.constants.message import (INVALID_PHONE_NUMBER, INVALID_EMAIL_ID, USER_PHONE_EXISTS, USER_EMAIL_EXISTS,
                                    BAD_REQUEST, USER_SUCCESSFULLY_REGISTERED, USER_DOES_NOT_EXISTS,
                                    SUCCESSFULLY_UPDATED_USER)
from custom_security.authorization import PublicAPIPermission, JWTAuthentication
from error_logging.db_log_handler import log_error
from exception_handler.generic_exception import GenericException, CustomBadRequest, CustomNotFound
from .models import Users
from .serializers import RegistrationSerializer, UserProfileSerializer, UpdateUserSerializer, PasswordResetSerializer
from .utils import is_valid_mobile_number, is_valid_email, bcrypt_hash_password

# Error-code: 11xxx
STATIC_UUID = "3f7061f6-3eba-11ee-be56-0242ac120002"


# API for user registration
class RegistrationView(APIView):
    permission_classes = [PublicAPIPermission]

    def post(self, request):
        try:
            with transaction.atomic():
                registration_serializer = RegistrationSerializer(data=request.data)

                if registration_serializer.is_valid():
                    # Validating mobile number and email
                    if not is_valid_mobile_number(request.data["mobile_no"]):
                        return CustomBadRequest(message=INVALID_PHONE_NUMBER)

                    if not is_valid_email(request.data["email"]):
                        return CustomBadRequest(message=INVALID_EMAIL_ID)
                    
                    # Checking if mobile number and email already exist
                    if Users.objects.filter(mobile_no=request.data["mobile_no"]).exists():
                        return CustomBadRequest(message=USER_PHONE_EXISTS)
                    
                    if Users.objects.filter(email=request.data["email"]).exists():
                        return CustomBadRequest(message=USER_EMAIL_EXISTS)
                
                    user = registration_serializer.save()

                    authentication_tokens = get_authentication_tokens(user)

                    save_auth_tokens(authentication_tokens)

                    return GenericSuccessResponse(message=USER_SUCCESSFULLY_REGISTERED,
                                                  data=authentication_tokens,
                                                  status=status.HTTP_201_CREATED)
                
                else:
                    return CustomBadRequest(message=BAD_REQUEST)

        except Exception as e:
            log_error(e, 11000)
            return GenericException()


# API for user profile
class UserProfile(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            current_user = request.user
            if current_user is None:
                return CustomNotFound(message=USER_DOES_NOT_EXISTS)
            else:
                user_profile = UserProfileSerializer(instance=current_user)
                return GenericSuccessResponse(data=user_profile.data, status=status.HTTP_200_OK)

        except Exception as e:
            log_error(e, 11000)
            return GenericException()

    def patch(self, request):
        try:
            with transaction.atomic():
                user = request.user

                if "password" in request.data and request.data["password"] is not None:
                    hash_password = bcrypt_hash_password(request.data["password"])
                    request.data.update({
                        "password": hash_password
                        })

                user_serializer = UpdateUserSerializer(data=request.data, partial=True)
                if user_serializer.is_valid():
                    if "mobile_no" in request.data and request.data["mobile_no"] is not None:
                        if not is_valid_mobile_number(request.data["mobile_no"]):
                            return CustomBadRequest(message=INVALID_PHONE_NUMBER)
                        
                        if Users.objects.filter(mobile_no=request.data["mobile_no"]).exists():
                            return CustomBadRequest(message=USER_PHONE_EXISTS)

                    user_serializer.update(user, user_serializer.validated_data)

                    return GenericSuccessResponse(message=SUCCESSFULLY_UPDATED_USER,
                                                  status=status.HTTP_200_OK)
                
                else:
                    return CustomBadRequest(message=BAD_REQUEST)

        except Exception as e:
            log_error(e, 11000)
            return GenericException()


# API for initiating password reset
class InitiateResetPassword(APIView):
    permission_classes = [PublicAPIPermission]

    def post(self, request):
        try:
            serializer = PasswordResetSerializer(data=request.data)
            
            if serializer.is_valid():
                email = serializer.validated_data['email']
                
                try:
                    user = Users.objects.get(email=email)
                    
                    token = str(user.mobile_no) + STATIC_UUID + str(user.user_id)
                    uid = urlsafe_base64_encode(force_bytes(user.user_id))
                    reset_url = f"http://127.0.0.1:8000/api/v1/users/initiate-reset/{uid}/{token}/"

                    send_mail(
                        'Password Reset',
                        f'Click the link to reset your password: {reset_url}',
                        EMAIL_HOST,
                        [user.email],
                        fail_silently=False,
                    )
                    return GenericSuccessResponse(message="Password reset email sent",
                                                  status=status.HTTP_200_OK)
                
                except Users.DoesNotExist:
                    return CustomBadRequest(message="User with this email does not exist",
                                            status=status.HTTP_400_BAD_REQUEST)
            
            else:
                return CustomBadRequest(message=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            log_error(e, 11000)
            return GenericException()

# API for resetting password
class ResetPasswordView(APIView):
    def get(self, request, uid, token):
        return render(request, 'reset_password_form.html')

    def post(self, request, uid, token):
        try:
            user_id = str(urlsafe_base64_decode(uid), 'utf-8')
            user = Users.objects.get(user_id=user_id)

            generated_token = str(user.mobile_no) + STATIC_UUID + str(user.user_id)

            if generated_token == token:
                new_password = request.data.get('new_password')
                confirm_password = request.data.get('confirm_password')

                if new_password == confirm_password:
                    hashed_password = bcrypt_hash_password(new_password)
                    user.password = hashed_password
                    user.save()
                    
                    return JsonResponse({'message': 'Password reset successfully'}, status=200)

                else:
                    return JsonResponse({'message': 'Passwords do not match'}, status=400)

            else:
                return CustomBadRequest(message="Invalid user ID", status=status.HTTP_400_BAD_REQUEST)

        except Users.DoesNotExist:
            return JsonResponse({'message': 'Invalid user ID'}, status=400)
                
        except Exception as e:
            log_error(e, 11000)
            return GenericException()
