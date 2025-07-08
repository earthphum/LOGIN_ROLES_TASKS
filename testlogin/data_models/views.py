# data_models/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import CustomerProfile, Vehicle
from .serializers import CustomerProfileSerializer, VehicleSerializer


class CustomerProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]
