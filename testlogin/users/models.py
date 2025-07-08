from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        ADMIN_LIMITED = "ADMIN_LIMITED", "Admin (Limited)"
        AGENT = "AGENT", "Agent"
        VIEWER = "VIEWER", "Viewer"

    role = models.CharField(max_length=50, choices=Role.choices, default=Role.VIEWER)