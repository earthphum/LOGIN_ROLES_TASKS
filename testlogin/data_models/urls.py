# data_models/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerProfileViewSet, VehicleViewSet

router = DefaultRouter()
router.register(r"customers", CustomerProfileViewSet)
router.register(r"vehicles", VehicleViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
