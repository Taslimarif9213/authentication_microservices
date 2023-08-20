from django.urls import path

from authentication.views import Login, Logout


urlpatterns = [
    path("login", Login.as_view()),
    path("logout", Logout.as_view()),
]
