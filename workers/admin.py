from django.contrib import admin

from .models import WorkerProfile


@admin.register(WorkerProfile)
class WorkerProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "phone_number",
        "experience_years",
        "rate",
        "pricing_type",
        "verification_status",
        "is_available",
        "created_at",
    )

    list_filter = (
        "verification_status",
        "pricing_type",
        "is_available",
    )

    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
        "phone_number",
    )

    filter_horizontal = (
        "skills",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )