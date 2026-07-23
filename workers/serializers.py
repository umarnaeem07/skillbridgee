from rest_framework import serializers

from .models import WorkerProfile
from skills.models import Skill


class WorkerProfileCreateSerializer(serializers.ModelSerializer):

    skills = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.filter(is_active=True),
        many=True
    )

    class Meta:

        model = WorkerProfile

        fields = (
            "phone_number",
            "profile_image",
            "bio",
            "experience_years",
            "rate",
            "pricing_type",
            "address",
            "latitude",
            "longitude",
            "skills",
        )

    def create(self, validated_data):

        skills = validated_data.pop("skills")

        worker_profile = WorkerProfile.objects.create(
            user=self.context["request"].user,
            **validated_data
        )

        worker_profile.skills.set(skills)

        return worker_profile
from rest_framework import serializers

from .models import WorkerProfile


class WorkerProfileSerializer(serializers.ModelSerializer):

    skills = serializers.StringRelatedField(
        many=True
    )

    class Meta:

        model = WorkerProfile

        fields = "__all__"

        depth = 1

class WorkerProfileUpdateSerializer(serializers.ModelSerializer):

    skills = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.filter(is_active=True),
        many=True,
        required=False
    )

    class Meta:

        model = WorkerProfile

        exclude = (
            "user",
            "verification_status",
            "created_at",
            "updated_at",
        )