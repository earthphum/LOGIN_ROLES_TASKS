# tasks/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.contenttypes.models import ContentType

# ส่วนที่ใช้สำหรับ Real-time (Channels)
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# import Models
from .models import Task, SubTask
from data_models.models import CustomerProfile, Vehicle

# import Serializers
from .serializers import TaskSerializer, TaskCreateSerializer, TaskRejectSerializer

# import Permissions
from users.permissions import IsAdminRole, IsAdminOrAdminLimitedRole


# ฟังก์ชันช่วยสำหรับส่งข้อมูลอัปเดตผ่าน WebSocket
def broadcast_task_update(data):
    """ฟังก์ชันช่วยสำหรับส่งข้อมูลอัปเดต"""
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "tasks_group",
        {"type": "task.update", "data": data},
    )


class TaskViewSet(viewsets.ModelViewSet):
    queryset = (
        Task.objects.all()
        .select_related("requester", "approver")
        .prefetch_related("subtasks")
        .order_by("-created_at")
    )

    def get_serializer_class(self):
        if self.action == "create":
            return TaskCreateSerializer
        if self.action == "reject":
            return TaskRejectSerializer
        return TaskSerializer

    def get_permissions(self):
        """กำหนด Permission ตาม action"""
        if self.action in ["approve", "reject", "destroy"]:
            self.permission_classes = [IsAdminRole]
        elif self.action == "create":
            self.permission_classes = [IsAdminOrAdminLimitedRole]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        """
        ตอนสร้าง Task ใหม่: บันทึก requester และส่งข่าว
        """
        task = serializer.save(requester=self.request.user)
        broadcast_task_update({"action": "new_task", "task": TaskSerializer(task).data})

    @action(detail=True, methods=["post"], url_path="approve")
    def approve(self, request, pk=None):
        """Action สำหรับ Admin อนุมัติ Task"""
        task = self.get_object()
        if task.status != Task.Status.PENDING_APPROVAL:
            return Response(
                {"error": "Task นี้ไม่ได้อยู่ในสถานะรออนุมัติ"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        task.status = Task.Status.IN_PROGRESS
        task.approver = request.user
        task.save()

        # สร้าง Object ที่เกี่ยวข้อง
        customer = CustomerProfile.objects.create(
            full_name=f"Customer for Task {task.id}",
            email=f"task{task.id}@example.com",
            created_by=request.user,
        )
        vehicle = Vehicle.objects.create(
            license_plate=f"TASK-{task.id}",
            brand="N/A",
            model="N/A",
            owner=customer,
            registered_by=request.user,
        )
        SubTask.objects.create(
            task=task,
            title="ยืนยันข้อมูลโปรไฟล์ลูกค้า",
            content_type=ContentType.objects.get_for_model(CustomerProfile),
            object_id=customer.id,
        )
        SubTask.objects.create(
            task=task,
            title="ลงทะเบียนข้อมูลรถยนต์",
            content_type=ContentType.objects.get_for_model(Vehicle),
            object_id=vehicle.id,
        )

        # [แก้ไข] เพิ่มบรรทัดนี้เพื่อรีเฟรชข้อมูล task จากฐานข้อมูล
        task.refresh_from_db()

        # ตอนนี้ task object จะมีข้อมูล subtasks ที่เพิ่งสร้างแล้ว
        updated_task_data = TaskSerializer(task).data
        broadcast_task_update({"action": "task_approved", "task": updated_task_data})

        return Response(updated_task_data)

    @action(detail=True, methods=["post"], url_path="reject")
    def reject(self, request, pk=None):
        """Action สำหรับ Admin ปฏิเสธ Task"""
        task = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reason = serializer.validated_data["reason"]

        task.status = Task.Status.REJECTED
        task.approver = request.user
        task.rejection_reason = reason
        task.save()

        response_serializer = TaskSerializer(task)
        broadcast_task_update(
            {"action": "task_rejected", "task": response_serializer.data}
        )

        return Response(response_serializer.data)
