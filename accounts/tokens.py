from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import (
    urlsafe_base64_encode,
    urlsafe_base64_decode,
)

from .models import User


def generate_uid(user: User) -> str:
    """
    Generate a URL-safe Base64 encoded user ID.
    """
    return urlsafe_base64_encode(
        force_bytes(user.pk)
    )


def decode_uid(uidb64: str):
    """
    Decode the Base64 encoded user ID
    and return the corresponding User object.
    """

    try:
        uid = force_str(
            urlsafe_base64_decode(uidb64)
        )

        return User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return None


def generate_token(user: User) -> str:
    """
    Generate a secure email verification token.
    """
    return default_token_generator.make_token(user)


def verify_token(user: User, token: str) -> bool:
    """
    Verify whether the provided token
    is valid for the given user.
    """
    return default_token_generator.check_token(
        user,
        token
    )