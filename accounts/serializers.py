from rest_framework import serializers
from .email import send_verification_email
from .models import User
from .choices import UserRole
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .email import send_password_reset_email
class RegistrationSerializer(serializers.Serializer):

    email = serializers.EmailField()

    first_name = serializers.CharField(
        max_length=100
    )

    last_name = serializers.CharField(
        max_length=100
    )

    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    confirm_password = serializers.CharField(
        write_only=True
    )

    role = serializers.ChoiceField(
        choices=UserRole.choices
    )

    def validate_email(self, value):

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )

        return value

    def validate(self, attrs):

        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {
                    "confirm_password": "Passwords do not match."
                }
            )

        return attrs

    def create(self, validated_data):

        validated_data.pop("confirm_password")

        user = User.objects.create_user(
            **validated_data
        )
        send_verification_email(user)

        return user
    
class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs):

        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            email=email,
            password=password
        )

        if not user:
            raise serializers.ValidationError(
                "Invalid email or password."
            )

        if not user.is_email_verified:
            raise serializers.ValidationError(
                "Please verify your email first."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "Your account is inactive."
            )

        refresh = RefreshToken.for_user(user)

        return {
            "user": user,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
    
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "role",
            "is_email_verified",
        )

        read_only_fields = fields

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


class LogoutSerializer(serializers.Serializer):

    refresh = serializers.CharField()

    def save(self):

        refresh_token = self.validated_data["refresh"]

        token = RefreshToken(refresh_token)

        token.blacklist()

class ForgotPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()

    def save(self):

        email = self.validated_data["email"]

        try:
            user = User.objects.get(email=email)

            send_password_reset_email(user)
            

        except User.DoesNotExist:
            pass

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode



class ResetPasswordSerializer(serializers.Serializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    confirm_password = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs):

        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {
                    "confirm_password": "Passwords do not match."
                }
            )

        return attrs

    def save(self, uidb64, token):

        try:
            uid = urlsafe_base64_decode(uidb64).decode()

            user = User.objects.get(pk=uid)

        except Exception:
            raise serializers.ValidationError(
                {
                    "detail": "Invalid reset link."
                }
            )

        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError(
                {
                    "detail": "Reset link has expired or is invalid."
                }
            )

        user.set_password(
            self.validated_data["password"]
        )

        user.save()

        return user

class ChangePasswordSerializer(serializers.Serializer):

    current_password = serializers.CharField(
        write_only=True
    )

    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    confirm_password = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs):

        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {
                    "confirm_password":
                    "Passwords do not match."
                }
            )

        return attrs

    def save(self, user):

        if not user.check_password(
            self.validated_data["current_password"]
        ):

            raise serializers.ValidationError(
                {
                    "current_password":
                    "Current password is incorrect."
                }
            )

        if self.validated_data["password"] == self.validated_data["current_password"]:

            raise serializers.ValidationError(
                {
                    "password":
                    "New password must be different."
                }
            )

        user.set_password(
            self.validated_data["password"]
        )

        user.save()

        return user