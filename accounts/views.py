from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from .serializers import RegistrationSerializer
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
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role,
                    "is_email_verified": user.is_email_verified,
                }
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