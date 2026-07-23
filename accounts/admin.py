from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        "email",
        "first_name",
        "last_name",
        "role",
        "account_status",
        "is_email_verified",
        "is_active",
        "is_staff",
        "date_joined",
    )

    list_filter = (
        "role",
        "account_status",
        "is_email_verified",
        "is_active",
        "is_staff",
    )

    search_fields = (
        "email",
        "first_name",
        "last_name",
    )

    readonly_fields = (
        "id",
        "date_joined",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-date_joined",
    )