from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)
from .views import RegisterView, MeView

urlpatterns = [
    # регистрация
    path("register/", RegisterView.as_view(), name="auth-register"),

    # jwt
    path("login/", TokenObtainPairView.as_view(), name="auth-login"),          # вернёт access+refresh
    path("refresh/", TokenRefreshView.as_view(), name="auth-refresh"),
    path("verify/", TokenVerifyView.as_view(), name="auth-verify"),

    # текущий пользователь
    path("me/", MeView.as_view(), name="auth-me"),
]
