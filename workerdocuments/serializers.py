from rest_framework import serializers

from .models import WorkerDocument
from workers.choices import DocumentType


class WorkerDocumentUploadSerializer(serializers.Serializer):

    document_type = serializers.ChoiceField(
        choices=DocumentType.choices
    )

    file = serializers.FileField()


class WorkerDocumentSerializer(serializers.ModelSerializer):

    class Meta:

        model = WorkerDocument

        fields = (
            "id",
            "document_type",
            "file",
            "status",
            "remarks",
            "verified_at",
            "created_at",
        )

        read_only_fields = (
            "status",
            "remarks",
            "verified_at",
            "created_at",
        )

class RejectDocumentSerializer(serializers.Serializer):

    remarks = serializers.CharField()