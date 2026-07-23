from .models import WorkerDocument
from workers.choices import DocumentStatus

from django.utils import timezone

class WorkerDocumentService:

    @staticmethod
    def upload_document(worker, validated_data):

        document_type = validated_data["document_type"]

        uploaded_file = validated_data["file"]

        document, created = WorkerDocument.objects.get_or_create(

            worker=worker,

            document_type=document_type,

            defaults={
                "file": uploaded_file
            }
        )

        if not created:

            document.file = uploaded_file

            document.status = DocumentStatus.PENDING

            document.remarks = ""

            document.verified_by = None

            document.verified_at = None

            document.save()

        return document
    
    @staticmethod
    def get_worker_documents(worker):

        return WorkerDocument.objects.filter(
            worker=worker
        ).order_by("document_type")
    


    @staticmethod
    def approve_document(document, admin):

        document.status = DocumentStatus.APPROVED

        document.verified_by = admin

        document.verified_at = timezone.now()

        document.remarks = ""

        document.save()

        return document

    @staticmethod
    def reject_document(document, admin, remarks):

        document.status = DocumentStatus.REJECTED

        document.verified_by = admin

        document.verified_at = timezone.now()

        document.remarks = remarks

        document.save()

        return document