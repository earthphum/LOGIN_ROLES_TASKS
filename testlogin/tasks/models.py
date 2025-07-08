from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Task(models.Model):
    class Status(models.TextChoices):
        PENDING_APPROVAL = "PENDING_APPROVAL", "รออนุมัติ"
        IN_PROGRESS = "IN_PROGRESS", "กำลังดำเนินการ"
        COMPLETED = "COMPLETED", "เสร็จสิ้น"
        REJECTED = "REJECTED", "ปฏิเสธ"

    title = models.CharField(max_length=255, verbose_name="ชื่องาน")
    description = models.TextField(blank=True, null=True, verbose_name="รายละเอียด")
    status = models.CharField(
        max_length=50, choices=Status.choices, default=Status.PENDING_APPROVAL
    )

    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="requested_tasks",
        verbose_name="ผู้ร้องขอ",
    )
    approver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="approved_tasks",
        null=True,
        blank=True,
        verbose_name="ผู้อนุมัติ",
    )

    rejection_reason = models.TextField(
        blank=True, null=True, verbose_name="เหตุผลที่ปฏิเสธ"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}: {self.title}"

    def check_completion(self):
        """ตรวจสอบว่า Subtask ทั้งหมดเสร็จสิ้นหรือยัง"""
        all_subtasks = self.subtasks.all()
        if not all_subtasks:
            return

        is_completed = all(
            sub.status == SubTask.Status.COMPLETED for sub in all_subtasks
        )
        if is_completed:
            self.status = Task.Status.COMPLETED
            self.save()


class SubTask(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "รอทำ"
        COMPLETED = "COMPLETED", "เสร็จสิ้น"

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="subtasks")
    title = models.CharField(max_length=255, verbose_name="ชื่องานย่อย")
    status = models.CharField(
        max_length=50, choices=Status.choices, default=Status.PENDING
    )

    # Generic Foreign Key Fields
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        help_text="โมเดลเป้าหมาย (เช่น CustomerProfile, Vehicle)",
    )
    object_id = models.PositiveIntegerField(help_text="ID ของ object เป้าหมาย")
    target_object = GenericForeignKey("content_type", "object_id")

    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} for Task #{self.task.id}"
