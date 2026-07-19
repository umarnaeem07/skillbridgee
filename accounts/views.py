from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from .serializers import ChangePasswordSerializer, ForgotPasswordSerializer, LoginSerializer, LogoutSerializer, RegistrationSerializer, ResetPasswordSerializer, UserSerializer
from rest_framework.permissions import AllowAny

from .tokens import decode_uid, verify_token

class RegistrationAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = RegistrationSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.save()

        return Response(
            {
                "message": "Registration successful.",
                "user": UserSerializer(user).data    
                 
            },
            status=status.HTTP_201_CREATED
        )
    
class VerifyEmailAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):

        user = decode_uid(uidb64)

        if user is None:
            return Response(
                {
                    "message": "Invalid verification link."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not verify_token(user, token):
            return Response(
                {
                    "message": "Verification link is invalid or expired."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if user.is_email_verified:
            return Response(
                {
                    "message": "Email is already verified."
                },
                status=status.HTTP_200_OK
            )

        user.is_email_verified = True
        user.is_active = True
        user.save()

        return Response(
            {
                "message": "Email verified successfully."
            },
            status=status.HTTP_200_OK
        )
    
class LoginAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        data = serializer.validated_data

        user = data["user"]

        return Response(
            {
                "message": "Login successful.",
                "access": data["access"],
                "refresh": data["refresh"],
                "user": UserSerializer(user).data
            },
            status=status.HTTP_200_OK
        )
    
from rest_framework.permissions import IsAuthenticated


class MeAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserSerializer(
            request.user
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    
class LogoutAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = LogoutSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            {
                "message": "Logout successful."
            },
            status=status.HTTP_200_OK
        )
    
class ForgotPasswordAPIView(APIView):

    # on frontend, user will enter email, and we will send a password reset link to that email if the user exists. We will not reveal whether the user exists or not for security reasons.

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = ForgotPasswordSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            {
                "message": (
                    "If an account with that email exists, "
                    "a password reset link has been sent."
                )
            },
            status=status.HTTP_200_OK
        )
    
class ResetPasswordAPIView(APIView):
    # on frontend, user will click on the password reset link, which will take them to a page where they can enter a new password. The link will contain the uid and token, which we will use to verify the user and reset the password.

    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):

        serializer = ResetPasswordSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save(
            uidb64=uidb64,
            token=token
        )

        return Response(
            {
                "message": "Password reset successful."
            },
            status=status.HTTP_200_OK
        )
    
class ChangePasswordAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ChangePasswordSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save(
            request.user
        )

        return Response(
            {
                "message":
                "Password changed successfully."
            },
            status=status.HTTP_200_OK
        )