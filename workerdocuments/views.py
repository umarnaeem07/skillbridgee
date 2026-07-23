from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from workerdocuments.models import WorkerDocument
from workers.permissions import IsAdmin, IsWorker

from .serializers import (
    RejectDocumentSerializer,
    WorkerDocumentUploadSerializer,
    WorkerDocumentSerializer,
)
from django.shortcuts import get_object_or_404
from .services import WorkerDocumentService


class WorkerDocumentUploadAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsWorker,
    ]

    def post(self, request):

        serializer = WorkerDocumentUploadSerializer(

            data=request.data

        )

        serializer.is_valid(

            raise_exception=True

        )

        document = WorkerDocumentService.upload_document(

            worker=request.user.worker_profile,

            validated_data=serializer.validated_data

        )

        return Response(

            {
                "message": "Document uploaded successfully.",

                "document": WorkerDocumentSerializer(
                    document
                ).data
            },

            status=status.HTTP_201_CREATED
        )
class WorkerDocumentListAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsWorker,
    ]

    def get(self, request):

        documents = WorkerDocumentService.get_worker_documents(
            request.user.worker_profile
        )

        serializer = WorkerDocumentSerializer(
            documents,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
class ApproveWorkerDocumentAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin,
    ]

    def patch(
        self,
        request,
        pk
    ):

        document = get_object_or_404(
            WorkerDocument,
            pk=pk
        )

        document = WorkerDocumentService.approve_document(
            document,
            request.user
        )

        return Response(
            WorkerDocumentSerializer(document).data
        )
class RejectWorkerDocumentAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin,
    ]

    def patch(
        self,
        request,
        pk
    ):

        serializer = RejectDocumentSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        document = get_object_or_404(
            WorkerDocument,
            pk=pk
        )

        document = WorkerDocumentService.reject_document(
            document=document,
            admin=request.user,
            remarks=serializer.validated_data["remarks"]
        )

        return Response(
            WorkerDocumentSerializer(document).data
        )