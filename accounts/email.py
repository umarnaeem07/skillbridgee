from django.conf import settings
from django.core.mail import send_mail

from .tokens import generate_uid, generate_token


def send_verification_email(user):

    uid = generate_uid(user)

    token = generate_token(user)

    verification_link = (
        f"{settings.BACKEND_URL}"
        f"/api/accounts/verify-email/"
        f"{uid}/{token}/"
    )

    subject = "Verify your SkillBridge account"

    message = f"""
Hi {user.first_name},

Welcome to SkillBridge!

Please click the link below to verify your email.

{verification_link}

If you did not create this account, please ignore this email.

Thanks,
SkillBridge Team
"""

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

def send_password_reset_email(user):

    uid = generate_uid(user)

    token = generate_token(user)

    reset_link = (
        f"{settings.BACKEND_URL}"
        f"/api/auth/reset-password/"
        f"{uid}/{token}/"
    )

    subject = "Reset your SkillBridge password"

    message = f"""
Hi {user.first_name},

We received a request to reset your SkillBridge password.

Click the link below to reset your password:

{reset_link}

If you didn't request a password reset, you can safely ignore this email.

Thanks,
SkillBridge Team
"""

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )