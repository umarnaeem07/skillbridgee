from rest_framework.permissions import BasePermission

from accounts.choices import UserRole


class IsWorker(BasePermission):

    message = "Only workers can perform this action."

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.role == UserRole.WORKER
        )
class IsAdmin(BasePermission):

    message = "Only admins can perform this action."

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.role == UserRole.ADMIN
        )
class IsCustomer(BasePermission):

    message = "Only customers can perform this action."

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.role == UserRole.CUSTOMER
        )