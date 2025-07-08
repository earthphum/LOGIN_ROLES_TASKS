from django.db import models
from django.conf import settings


class CustomerProfile(models.Model):
    """โมเดลตัวอย่าง: ข้อมูลลูกค้า"""

    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class Vehicle(models.Model):
    """โมเดลตัวอย่าง: ข้อมูลรถยนต์"""

    license_plate = models.CharField(max_length=20, unique=True)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    owner = models.ForeignKey(
        CustomerProfile, on_delete=models.CASCADE, related_name="vehicles"
    )
    registered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT
    )
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.license_plate} ({self.brand})"
