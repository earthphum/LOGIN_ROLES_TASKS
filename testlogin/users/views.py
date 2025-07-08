from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from .serializers import UserSerializer, UserCreateSerializer
from .permissions import IsAdminRole
# vvvv เพิ่ม 2 บรรทัดนี้ vvvv
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


# Endpoint สำหรับให้คนทั่วไปสมัครสมาชิก
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny] # ไม่ต้อง Login ก็สมัครได้

# Endpoint สำหรับให้ Admin จัดการ User ทั้งหมด
class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    permission_classes = [IsAdminRole] # ต้องเป็น Admin เท่านั้น

    # เลือก Serializer ให้ถูก
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

# vvvv เพิ่มฟังก์ชันนี้เข้าไปทั้งหมด vvvv
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_details(request):
    """
    API endpoint to get details of the currently logged-in user.
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)
