import jwt
from django.conf import settings
from django.db.models import Q

from rest_framework import authentication
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from rest_framework.permissions import BasePermission

from authentication.models import AuthTokens
from core.constants.message import TOKEN_EXPIRED
from error_logging.db_log_handler import log_error
from exception_handler.generic_exception import GenericException
from users.models import Users

# Error-code: 1xxx


class PublicAPIPermission(BasePermission):
    def has_permission(self, request, view):
        try:
            public_api_key = request.headers.get("public-key")
            if public_api_key == settings.PUBLIC_API_KEY:
                return True
            else:
                raise PermissionDenied()

        except PermissionDenied as e:
            log_error(e, 1400)
            raise PermissionDenied()

        except Exception as e:
            log_error(e, 1000)
            raise e


def token_decode(token):
    try:
        claims = jwt.decode(token, settings.JWT_SECRET, algorithms=settings.JWT_ALGORITHM)

        if not AuthTokens.objects.filter(Q(access_token=token) | Q(refresh_token=token)).exists():
            raise AuthenticationFailed(detail=TOKEN_EXPIRED)

        if "user_id" not in claims:
            raise AuthenticationFailed(detail=TOKEN_EXPIRED)

        user = Users.objects.get(user_id=claims["user_id"], mobile_no=claims["mobile_no"])

        return user, claims

    except Users.DoesNotExist as e:
        raise AuthenticationFailed(detail=TOKEN_EXPIRED)

    except AuthenticationFailed as e:
        raise AuthenticationFailed(e.detail)

    except jwt.ExpiredSignatureError as e:
        raise AuthenticationFailed(detail=TOKEN_EXPIRED)
    except jwt.exceptions.InvalidSignatureError as e:
        raise AuthenticationFailed(detail=TOKEN_EXPIRED)
    except Exception as e:
        log_error(e, 1000)
        raise e
    

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:
            if "authorization" not in request.headers:
                raise PermissionDenied()

            token = request.headers.get("authorization").split(" ")[1]

            return token_decode(token)

        except PermissionDenied as e:
            log_error(e, 1410)
            raise PermissionDenied()

        except Users.DoesNotExist as e:
            raise AuthenticationFailed(detail=TOKEN_EXPIRED)

        except AuthenticationFailed as e:
            raise AuthenticationFailed(e.detail)

        except jwt.ExpiredSignatureError as e:
            raise AuthenticationFailed(detail=TOKEN_EXPIRED)

        except jwt.exceptions.DecodeError as e:
            raise AuthenticationFailed(detail=TOKEN_EXPIRED)

        except Exception as e:
            log_error(e, 1000)
            return GenericException()
        