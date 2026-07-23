from django.contrib import admin

from .models import WorkerDocument


@admin.register(WorkerDocument)
class WorkerDocumentAdmin(admin.ModelAdmin):

    list_display = (
        "worker",
        "document_type",
        "status",
        "verified_by",
        "verified_at",
        "created_at",
    )

    list_filter = (
        "document_type",
        "status",
    )

    search_fields = (
        "worker__user__email",
        "worker__user__first_name",
        "worker__user__last_name",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )