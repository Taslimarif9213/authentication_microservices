import jwt
import datetime

from django.conf import settings
from .serializers import AuthTokenSerializer


def save_auth_tokens(authentication_tokens):
    auth_token_serializer = AuthTokenSerializer(data=authentication_tokens)
    if auth_token_serializer.is_valid():
        auth_token_serializer.save()


def get_authentication_tokens(user):
    access_token = jwt.encode({"user_id": user.user_id,
                               "mobile_no": user.mobile_no,
                               "exp": datetime.datetime.now(tz=datetime.timezone.utc) + settings.ACCESS_TOKEN_LIFETIME,
                               "type": "access"},
                              settings.JWT_SECRET,
                              algorithm=settings.JWT_ALGORITHM)

    refresh_token = jwt.encode({"user_id": user.user_id,
                                "mobile_no": user.mobile_no,
                                "exp": datetime.datetime.now(
                                    tz=datetime.timezone.utc) + settings.REFRESH_TOKEN_LIFETIME,
                                "type": "refresh"},
                               settings.JWT_SECRET,
                               algorithm=settings.JWT_ALGORITHM)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "access_token_expiry": settings.ACCESS_TOKEN_LIFETIME,
        "refresh_token_expiry": settings.REFRESH_TOKEN_LIFETIME
    }
