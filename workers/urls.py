from django.urls import path

from .views import (
    WorkerProfileCreateAPIView,
    WorkerProfileAPIView,
    WorkerProfileUpdateAPIView,
)

urlpatterns = [
    path(
        "profile/",
        WorkerProfileCreateAPIView.as_view()
    ),

    path(
        "profile/me/",
        WorkerProfileAPIView.as_view()
    ),

    path(
        "profile/update/",
        WorkerProfileUpdateAPIView.as_view()
    ),
]