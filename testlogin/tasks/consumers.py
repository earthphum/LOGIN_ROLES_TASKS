# tasks/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer


class TaskConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # เข้าร่วมกลุ่ม "tasks_group"
        await self.channel_layer.group_add("tasks_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # ออกจากกลุ่ม
        await self.channel_layer.group_discard("tasks_group", self.channel_name)

    # ฟังก์ชันนี้จะถูกเรียกเมื่อได้รับ message จาก Channel Layer
    async def task_update(self, event):
        # ส่งข้อมูลไปยัง Client (Frontend)
        await self.send(text_data=json.dumps(event["data"]))
