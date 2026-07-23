from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import WorkerProfile
from .permissions import IsWorker
from .serializers import (
    WorkerProfileCreateSerializer,
    WorkerProfileSerializer,
    WorkerProfileUpdateSerializer,
)


class WorkerProfileCreateAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsWorker,
    ]

    def post(self, request):

        if WorkerProfile.objects.filter(
            user=request.user
        ).exists():

            return Response(
                {
                    "message": "Worker profile already exists."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = WorkerProfileCreateSerializer(
            data=request.data,
            context={
                "request": request
            }
        )

        serializer.is_valid(
            raise_exception=True
        )

        worker_profile = serializer.save()

        return Response(
            {
                "message": "Worker profile created successfully.",
                "worker_profile": WorkerProfileSerializer(
                    worker_profile
                ).data
            },
            status=status.HTTP_201_CREATED
        )


class WorkerProfileAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsWorker,
    ]

    def get(self, request):

        try:

            worker_profile = request.user.worker_profile

        except WorkerProfile.DoesNotExist:

            return Response(
                {
                    "message": "Worker profile not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = WorkerProfileSerializer(
            worker_profile
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class WorkerProfileUpdateAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsWorker,
    ]

    def patch(self, request):

        try:

            worker_profile = request.user.worker_profile

        except WorkerProfile.DoesNotExist:

            return Response(
                {
                    "message": "Worker profile not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = WorkerProfileUpdateSerializer(
            worker_profile,
            data=request.data,
            partial=True
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            {
                "message": "Worker profile updated successfully.",
                "worker_profile": WorkerProfileSerializer(
                    worker_profile
                ).data
            },
            status=status.HTTP_200_OK
        )


class WorkerProfileDeleteAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsWorker,
    ]

    def delete(self, request):

        try:

            worker_profile = request.user.worker_profile

        except WorkerProfile.DoesNotExist:

            return Response(
                {
                    "message": "Worker profile not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        worker_profile.delete()

        return Response(
            {
                "message": "Worker profile deleted successfully."
            },
            status=status.HTTP_204_NO_CONTENT
        )