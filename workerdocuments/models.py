import uuid

from django.db import models

from accounts.models import User
from workers.models import WorkerProfile
from workers.choices import DocumentType, DocumentStatus


class WorkerDocument(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    worker = models.ForeignKey(
        WorkerProfile,
        on_delete=models.CASCADE,
        related_name="documents"
    )

    document_type = models.CharField(
        max_length=30,
        choices=DocumentType.choices
    )

    file = models.FileField(
        upload_to="worker_documents/"
    )

    status = models.CharField(
        max_length=20,
        choices=DocumentStatus.choices,
        default=DocumentStatus.PENDING
    )

    remarks = models.TextField(
        blank=True
    )

    verified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_documents"
    )

    verified_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ["-created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["worker", "document_type"],
                name="unique_document_per_worker"
            )
        ]

    def __str__(self):

        return f"{self.worker.user.email} - {self.document_type}"