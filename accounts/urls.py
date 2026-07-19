from .views import LoginAPIView, RegistrationAPIView , VerifyEmailAPIView , MeAPIView , LogoutAPIView , ForgotPasswordAPIView , ResetPasswordAPIView , ChangePasswordAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path

urlpatterns = [
    path("register/", RegistrationAPIView.as_view(), name="register"),
    path("forgot-password/", ForgotPasswordAPIView.as_view(), name="forgot-password"),
    path("reset-password/<str:uidb64>/<str:token>/", ResetPasswordAPIView.as_view(), name="reset-password"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("change-password/", ChangePasswordAPIView.as_view(), name="change-password"),
    path("me/", MeAPIView.as_view(), name="me"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("verify-email/<str:uidb64>/<str:token>/", VerifyEmailAPIView.as_view(), name="verify-email"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]