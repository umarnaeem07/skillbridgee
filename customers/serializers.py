from .models import CustomerProfile
from rest_framework import serializers


class CreateCustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerProfile
        fields = "__all__"

    def create(self, validated_data):
        customer = CustomerProfile.objects.create(
            user=self.context["request"].user,
            **validated_data
        )
        return customer    

class CustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomerProfile
        fields = "__all__"

class CustomerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = "__all__"
    