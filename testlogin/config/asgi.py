# your_project/asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
import tasks.routing  # <-- Import routing ของแอป tasks

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            URLRouter(tasks.routing.websocket_urlpatterns)
        ),
    }
)
