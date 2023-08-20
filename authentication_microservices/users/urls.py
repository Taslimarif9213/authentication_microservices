from django.urls import path

from .views import RegistrationView, UserProfile, InitiateResetPassword, ResetPasswordView


urlpatterns = [
    path("registration", RegistrationView.as_view()),
    path("profile", UserProfile.as_view()),
    path('initiate-reset/', InitiateResetPassword.as_view(), name='initiate-reset'),
    path('initiate-reset/<str:uid>/<str:token>/', ResetPasswordView.as_view(), name='password_reset_confirm')
]
