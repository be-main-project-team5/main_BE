import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()  # 이 부분이 핵심입니다.

# Django 설정이 로드된 후에 라우팅을 임포트합니다.
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import apps.chats.routing
from apps.common.middlewares import JWTAuthMiddlewareStack

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": JWTAuthMiddlewareStack(URLRouter(apps.chats.routing.websocket_urlpatterns)),
    }
)
