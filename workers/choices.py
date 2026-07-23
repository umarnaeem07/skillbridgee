from django.db import models


class PricingType(models.TextChoices):
    HOURLY = "hourly", "Hourly"
    DAILY = "daily", "Daily"
    FIXED = "fixed", "Fixed"


class VerificationStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"




class DocumentType(models.TextChoices):

    CNIC_FRONT = "cnic_front", "CNIC Front"

    CNIC_BACK = "cnic_back", "CNIC Back"

    SELFIE = "selfie", "Selfie"

class DocumentStatus(models.TextChoices):

    PENDING = "pending", "Pending"

    APPROVED = "approved", "Approved"

    REJECTED = "rejected", "Rejected"