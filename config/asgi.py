import os

import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from apps.common.middlewares import JWTAuthMiddlewareStack

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()  # 이 부분이 핵심입니다.

# Django 설정이 로드된 후에 라우팅을 임포트합니다.
import apps.chats.routing

django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": JWTAuthMiddlewareStack(URLRouter(apps.chats.routing.websocket_urlpatterns)),
    }
)
