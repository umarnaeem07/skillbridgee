from django.db import models


class UserRole(models.TextChoices):
    ADMIN = "admin", "Admin"
    CUSTOMER = "customer", "Customer"
    WORKER = "worker", "Worker"

class AccountStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    DEACTIVATED = "deactivated", "Deactivated"
    SUSPENDED = "suspended", "Suspended"