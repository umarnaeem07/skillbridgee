from django.urls import path

from .views import ApproveWorkerDocumentAPIView, WorkerDocumentUploadAPIView, WorkerDocumentListAPIView , RejectWorkerDocumentAPIView


urlpatterns = [

    path(

        "",

        WorkerDocumentUploadAPIView.as_view(),

        name="upload-document"

    ),
    path(
        "my/",
        WorkerDocumentListAPIView.as_view(),
        name="my-documents"
    ),
    path(
        "approve/<int:pk>/",
        ApproveWorkerDocumentAPIView.as_view(),
        name="approve-document"
    ),
    path(
        "reject/<int:pk>/",
        RejectWorkerDocumentAPIView.as_view(),
        name="reject-document"
    )

]