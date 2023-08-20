from django.urls import path

from authentication.views import Login, Logout, LogingWithPassword


urlpatterns = [
    path("login", Login.as_view()),
    path("login/password", LogingWithPassword.as_view()),    
    path("logout", Logout.as_view())
]
