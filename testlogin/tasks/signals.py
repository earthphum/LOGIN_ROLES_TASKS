# tasks/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

# [เพิ่ม] import สิ่งที่จำเป็นสำหรับ broadcast
from .views import broadcast_task_update
from .serializers import TaskSerializer

from .models import SubTask
from data_models.models import CustomerProfile, Vehicle


def update_subtask_status(sender, instance):
    """
    [แก้ไข] ฟังก์ชันกลางสำหรับอัปเดต SubTask และส่งข่าว
    """
    content_type = ContentType.objects.get_for_model(sender)
    subtasks_to_update = SubTask.objects.filter(
        content_type=content_type, object_id=instance.id, status=SubTask.Status.PENDING
    )

    task_to_broadcast = None

    for subtask in subtasks_to_update:
        subtask.status = SubTask.Status.COMPLETED
        subtask.completed_at = timezone.now()
        subtask.save()

        # หลังจากอัปเดต Subtask ให้ตรวจสอบ Task หลักทันที
        subtask.task.check_completion()
        task_to_broadcast = subtask.task

    # [เพิ่ม] ถ้ามีการอัปเดต ให้ส่งข่าวเพียงครั้งเดียว
    if task_to_broadcast:
        broadcast_task_update(
            {
                "action": "task_progress_update",
                "task": TaskSerializer(task_to_broadcast).data,
            }
        )


# เชื่อม Signal เข้ากับโมเดลเป้าหมาย
@receiver(post_save, sender=CustomerProfile)
def on_customer_profile_save(sender, instance, created, **kwargs):
    # เราไม่ต้องการ trigger ตอนที่ approve view สร้าง object ครั้งแรก
    # เราจะเช็คว่าข้อมูลมีการเปลี่ยนแปลงจริง ๆ หรือไม่ (ไม่ใช่แค่สร้าง)
    # ในตัวอย่างนี้ เราจะรันทุกครั้งหลังการสร้าง เพื่อให้การทดสอบง่าย
    if not created:  # ทำงานเฉพาะตอนอัปเดต ไม่ใช่ตอนสร้าง
        update_subtask_status(sender, instance)


@receiver(post_save, sender=Vehicle)
def on_vehicle_save(sender, instance, created, **kwargs):
    if not created:  # ทำงานเฉพาะตอนอัปเดต ไม่ใช่ตอนสร้าง
        update_subtask_status(sender, instance)
