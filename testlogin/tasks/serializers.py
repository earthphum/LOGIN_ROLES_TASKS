from rest_framework import serializers
from .models import Task, SubTask
from users.serializers import UserSerializer  # import UserSerializer เดิมของคุณ


class SubTaskSerializer(serializers.ModelSerializer):
    """
    แก้ไข Serializer นี้เพื่อส่งข้อมูลที่จำเป็นให้ Frontend
    """

    # เพิ่ม 2 บรรทัดนี้
    content_type_model = serializers.CharField(
        source="content_type.model", read_only=True
    )

    class Meta:
        model = SubTask
        # เพิ่ม 'object_id' และ 'content_type_model' เข้าไปใน fields
        fields = (
            "id",
            "title",
            "status",
            "completed_at",
            "object_id",
            "content_type_model",
        )


class TaskSerializer(serializers.ModelSerializer):
    """Serializer สำหรับแสดงข้อมูล Task แบบละเอียด"""

    requester = UserSerializer(read_only=True)
    approver = UserSerializer(read_only=True)
    subtasks = SubTaskSerializer(many=True, read_only=True)
    # --- ลบบรรทัด status = ... ออกไปจากตรงนี้ ---

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "status",
            "requester",
            "approver",  # <-- ให้ 'status' ยังอยู่ใน fields
            "rejection_reason",
            "created_at",
            "updated_at",
            "subtasks",
        )


class TaskCreateSerializer(serializers.ModelSerializer):
    """Serializer สำหรับสร้าง Task โดย Admin Limited"""

    class Meta:
        model = Task
        fields = ("title", "description")


class TaskRejectSerializer(serializers.ModelSerializer):
    """Serializer สำหรับรับเหตุผลในการปฏิเสธ Task"""

    reason = serializers.CharField(write_only=True, required=True, label="เหตุผลที่ปฏิเสธ")

    class Meta:
        model = Task
        fields = ("reason",)
