from .views import RegistrationAPIView , VerifyEmailAPIView

from django.urls import path

urlpatterns = [
    path("register/", RegistrationAPIView.as_view(), name="register"),
    path("verify-email/<str:uidb64>/<str:token>/", VerifyEmailAPIView.as_view(), name="verify-email"),
]