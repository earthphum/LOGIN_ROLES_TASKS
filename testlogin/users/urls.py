# users/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegistrationView, AdminUserViewSet, get_user_details 

router = DefaultRouter()
router.register(r'manage', AdminUserViewSet, basename='admin-user')

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('admin/', include(router.urls)),
    path('me/', get_user_details, name='user-details'), # << เพิ่มบรรทัดนี้
]