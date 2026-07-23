from .models import CustomerProfile
from .serializers import CreateCustomerSerializer , CustomerSerializer, CustomerUpdateSerializer
# from rest_framework import viewsets
from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated
from workers.permissions import IsCustomer
from rest_framework import status


class CustomerCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request):

        if CustomerProfile.objects.filter(user=request.user).exists():
            return Response(
                {
                    "message": "Customer profile already exists."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = CreateCustomerSerializer(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()
        return Response(
            {
                "message": "Customer created successfully.",
                "customer": CustomerSerializer(customer).data
            },
            status=status.HTTP_201_CREATED
        )
    
class CustomerAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def get(self, request):
        try:
            customer = CustomerProfile.objects.get(user=request.user)
        except CustomerProfile.DoesNotExist:
            return Response(
                {
                    "message": "Customer profile does not exist."
                },
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CustomerSerializer(customer)
        return Response(
            {
                "customer": serializer.data
            },
            status=status.HTTP_200_OK
        )
    
class CustomerUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def patch(self, request):
        
        try:
            customer = request.user.customer_profile
        except CustomerProfile.DoesNotExist:
            return Response(
                {
                    "message": "Customer profile does not exist."
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = CustomerUpdateSerializer(
            customer,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()
        return Response(
            {
                "message": "Customer profile updated successfully.",
                "customer": CustomerSerializer(customer).data
            },
            status=status.HTTP_200_OK
        )