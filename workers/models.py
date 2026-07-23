import uuid

from django.db import models

from accounts.models import User
from skills.models import Skill
from .choices import PricingType, VerificationStatus

class WorkerProfile(models.Model):

   

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="worker_profile"
    )

    skills = models.ManyToManyField(
        Skill,
        related_name="workers"
    )

    phone_number = models.CharField(
        max_length=20
    )

    profile_image = models.ImageField(
        upload_to="workers/profile_images/",
        blank=True,
        null=True
    )

    bio = models.TextField()

    experience_years = models.PositiveIntegerField()

    rate = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    pricing_type = models.CharField(
        max_length=20,
        choices=PricingType.choices,
        default=PricingType.HOURLY
    )

    address = models.CharField(
        max_length=255
    )

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6
    )

    is_available = models.BooleanField(
        default=True
    )

    verification_status = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.user.email