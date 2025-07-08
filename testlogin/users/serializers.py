from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """Serializer สำหรับแสดงข้อมูล User"""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role')

class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer สำหรับสร้าง User พร้อม Hashing รหัสผ่าน"""
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'role')
        extra_kwargs = {
            'role': {'required': False} # Admin สามารถกำหนด Role ตอนสร้างได้
        }

    def create(self, validated_data):
        role = validated_data.pop('role', User.Role.VIEWER) # ถ้าไม่ส่ง role มา, ให้เป็น VIEWER
        user = User.objects.create_user(**validated_data) # ใช้ create_user เพื่อ hash password
        user.role = role
        user.save()
        return user