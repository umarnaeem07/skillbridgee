from .views import CustomerCreateAPIView, CustomerAPIView, CustomerUpdateAPIView
from django.urls import path

urlpatterns = [
    path('create/', CustomerCreateAPIView.as_view(), name='customer-create'),
    path('profile/', CustomerAPIView.as_view(), name='customer-profile'),
    path('update/', CustomerUpdateAPIView.as_view(), name='customer-update'),
]