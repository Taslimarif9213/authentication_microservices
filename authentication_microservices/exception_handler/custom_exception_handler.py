from rest_framework import status
from rest_framework.views import exception_handler


# Custom Exception handler will handle the response of Permission Denied Exception,
# AuthenticationFailed Exception, BadRequest, and NotFound Exceptions
def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None and response.status_code == status.HTTP_403_FORBIDDEN:
        response.data = {
            "data": [],
            "status": {
                "code": status.HTTP_403_FORBIDDEN,
                "message": response.data["detail"]
            }
        }

    if response is not None and response.status_code == status.HTTP_401_UNAUTHORIZED:
        response.data = {
            "data": [],
            "status": {
                "code": status.HTTP_401_UNAUTHORIZED,
                "message": response.data["detail"]
            }
        }

    if response is not None and response.status_code == status.HTTP_400_BAD_REQUEST:
        response.data = {
            "data": [],
            "status": {
                "code": status.HTTP_400_BAD_REQUEST,
                "message": response.data["detail"]
            }
        }

    if response is not None and response.status_code == status.HTTP_404_NOT_FOUND:
        response.data = {
            "data": [],
            "status": {
                "code": status.HTTP_404_NOT_FOUND,
                "message": response.data["detail"]
            }
        }

    if response is not None and response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        response.data = {
            "data": [],
            "status": {
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": response.data["detail"]
            }
        }

    return response
