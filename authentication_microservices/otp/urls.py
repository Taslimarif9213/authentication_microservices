from django.urls import path

from otp.views import GenerateOTP, OTPTypesView


urlpatterns = [
    path("generate", GenerateOTP.as_view()),
    path("types", OTPTypesView.as_view())
]
