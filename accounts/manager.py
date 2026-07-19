from django.contrib.auth.base_user import BaseUserManager

from .choices import UserRole


class UserManager(BaseUserManager):

    def create_user(
        self,
        email,
        first_name,
        last_name,
        password,
        role,
        **extra_fields
    ):
        if not email:
            raise ValueError("Email is required.")

        if not first_name:
            raise ValueError("First name is required.")

        if not last_name:
            raise ValueError("Last name is required.")

        if not password:
            raise ValueError("Password is required.")

        if not role:
            raise ValueError("Role is required.")

        email = self.normalize_email(email)

        # Default values for normal users
        extra_fields.setdefault("is_active", False)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_email_verified", False)
        extra_fields.setdefault("account_status", "active")

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(
        self,
        email,
        first_name,
        last_name,
        password,
        **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_email_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            role=UserRole.ADMIN,
            **extra_fields
        )