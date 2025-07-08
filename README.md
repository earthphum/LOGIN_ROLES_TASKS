# ระบบจัดการ Task แบบ Real-time (Django + Channels)

โปรเจกต์นี้คือระบบจัดการงาน (Task Management) ที่สร้างขึ้นด้วย Django โดยมีความสามารถในการอัปเดตสถานะของงานต่างๆ แบบ Real-time ผ่านเทคโนโลยี WebSocket ทำให้ผู้ใช้งานที่เกี่ยวข้องเห็นความคืบหน้าได้ทันทีโดยไม่ต้องรีเฟรชหน้าจอ

## ✨ คุณสมบัติหลัก (Features)

- **ระบบสิทธิ์ผู้ใช้งาน (User Roles):** แบ่งผู้ใช้งานออกเป็น 2 ระดับคือ
    - `ADMIN`: มีสิทธิ์อนุมัติ, ปฏิเสธ, และดูงานได้ทั้งหมด
    - `ADMIN_LIMITED`: มีสิทธิ์ในการสร้างงานใหม่ และทำงานย่อย (Subtask) ที่ได้รับมอบหมาย
- **Workflow การทำงาน:**
    1. `ADMIN_LIMITED` สร้าง Task ใหม่ (สถานะเริ่มต้น: *รออนุมัติ*)
    2. `ADMIN` จะได้รับการแจ้งเตือนแบบ Real-time ว่ามีงานใหม่เข้ามา
    3. `ADMIN` สามารถกด "อนุมัติ" หรือ "ปฏิเสธ" งานนั้นได้
    4. เมื่องานถูกอนุมัติ ระบบจะสร้างงานย่อย (Subtask) ที่เกี่ยวข้องให้โดยอัตโนมัติ (เช่น: ตรวจสอบข้อมูลลูกค้า, ลงทะเบียนรถยนต์)
    5. `ADMIN_LIMITED` สามารถกดทำงานย่อยแต่ละอย่างให้เสร็จสิ้นได้
    6. ทั้งสองฝั่งจะเห็นความคืบหน้าของ Subtask แบบ Real-time
    7. เมื่องานย่อยทั้งหมดเสร็จสิ้น สถานะของ Task หลักจะเปลี่ยนเป็น "เสร็จสิ้น" โดยอัตโนมัติ

## 🛠️ เทคโนโลยีที่ใช้ (Tech Stack)

- **Backend:**
    - Django
    - Django REST Framework (สำหรับสร้าง API)
    - Django Channels (สำหรับจัดการ WebSocket)
- **Real-time & Messaging:**
    - WebSockets
    - Redis (หรือ Valkey สำหรับ Arch Linux)
- **Frontend (สำหรับทดสอบ):**
    - HTML
    - JavaScript (Vanilla JS)

---

## 🚀 การติดตั้งและใช้งาน (Installation & Setup)

### 1. สิ่งที่ต้องมี (Prerequisites)

- Python 3.8+
- Redis (หรือ Valkey) ติดตั้งและทำงานอยู่บนเครื่อง

### 2. การตั้งค่าฝั่ง Backend (Django)

1.  **Clone โปรเจกต์:**
    ```bash
    git clone <your-repository-url>
    cd <your-project-folder>
    ```

2.  **สร้างและเปิดใช้งาน Virtual Environment:**
    ```bash
    # สร้าง venv
    python -m venv .venv
    # เปิดใช้งาน (macOS/Linux)
    source .venv/bin/activate
    # เปิดใช้งาน (Windows)
    .\venv\Scripts\activate
    ```

3.  **ติดตั้ง Dependencies:**
    ```bash
    pip install django djangorestframework channels channels-redis daphne djangorestframework-simplejwt django-cors-headers
    ```

4.  **ตั้งค่าฐานข้อมูลและ Migrate:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **สร้างผู้ใช้งาน:**
    สร้าง Superuser และผู้ใช้งานที่มี Role `ADMIN` และ `ADMIN_LIMITED`
    ```bash
    python manage.py createsuperuser
    # จากนั้นเข้าไปใน Admin Panel ([http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)) เพื่อสร้าง User อีก 2 คน
    # และกำหนด Role ให้ถูกต้อง
    ```

6.  **ตรวจสอบว่า Redis/Valkey ทำงานอยู่:**
    ```bash
    redis-cli ping
    # ควรจะตอบกลับมาว่า PONG
    ```

7.  **รันเซิร์ฟเวอร์ Django:**
    เซิร์ฟเวอร์จะทำงานด้วย `daphne` ซึ่งรองรับทั้ง HTTP และ WebSocket
    ```bash
    python manage.py runserver
    ```
    ตอนนี้ Backend ของคุณจะทำงานอยู่ที่ `http://127.0.0.1:8000`

### 3. การใช้งานฝั่ง Frontend (หน้าเว็บทดสอบ)

เนื่องจากหน้าเว็บทดสอบ (`realtime_tasks.html`) เป็นไฟล์ธรรมดา เราต้องรัน Web Server ง่ายๆ เพื่อให้เบราว์เซอร์อนุญาตการเชื่อมต่อ WebSocket

1.  **เปิด Terminal ใหม่**
2.  `cd` ไปยังโฟลเดอร์ที่เก็บไฟล์ `realtime_tasks.html`
3.  **รัน Local Web Server:** (เราจะรันที่ Port 8001 เพื่อไม่ให้ซ้ำกับ Django)
    ```bash
    python -m http.server 8001
    ```
4.  **เปิดเบราว์เซอร์** แล้วเข้าไปที่ URL:
    > **http://127.0.0.1:8001/realtime_tasks.html**

5.  **ทดสอบการทำงาน:**
    - Login ทั้งฝั่ง `ADMIN` และ `ADMIN_LIMITED`
    - ลองสร้าง Task ใหม่จากฝั่ง `ADMIN_LIMITED`
    - สังเกตว่า Task จะปรากฏขึ้นที่ฝั่ง `ADMIN` ทันที
    - กดอนุมัติที่ฝั่ง `ADMIN`
    - สังเกตว่าปุ่มสำหรับทำงาน Subtask จะปรากฏขึ้นที่ฝั่ง `ADMIN_LIMITED`
    - ลองกดทำงาน Subtask ให้เสร็จ แล้วดูสถานะที่เปลี่ยนไปของทั้งสองฝั่ง
