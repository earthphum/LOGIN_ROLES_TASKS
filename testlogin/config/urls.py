from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("api/users/", include("users.urls")),
    # Endpoints สำหรับ Login (รับ Token) และ Refresh Token
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include("tasks.urls")),  # <-- เพิ่ม URL ของแอป Task
    path("api/data/", include("data_models.urls")),  #
]
