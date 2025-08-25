from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from rest_framework_simplejwt.tokens import AccessToken
from urllib.parse import parse_qs

User = get_user_model()

@database_sync_to_async
def get_user(token):
    try:
        # AccessToken을 사용하여 토큰 검증 및 사용자 ID 추출
        access_token = AccessToken(token)
        user_id = access_token['user_id']
        user = User.objects.get(id=user_id)
        return user
    except Exception:
        return AnonymousUser()

class JwtAuthMiddleware:
    def __init__(self, app):
        # ASGI 애플리케이션을 저장합니다.
        self.app = app

    async def __call__(self, scope, receive, send):
        # HTTP 스코프인 경우 (웹소켓 핸드셰이크)
        if scope['type'] == 'websocket':
            close_old_connections() # 오래된 DB 연결 닫기 (필요시)
            
            # 쿼리 스트링에서 토큰 추출
            query_string = scope.get('query_string', b'').decode('utf-8')
            query_params = parse_qs(query_string)
            
            token = query_params.get('token')
            if token:
                # 토큰이 리스트 형태로 올 수 있으므로 첫 번째 값 사용
                token = token[0] if isinstance(token, list) else token
                scope['user'] = await get_user(token)
            else:
                scope['user'] = AnonymousUser()
        
        # 다음 미들웨어 또는 컨슈머로 요청을 전달합니다.
        return await self.app(scope, receive, send)

# 미들웨어 스택을 정의합니다.
# ProtocolTypeRouter와 URLRouter 사이에 이 미들웨어를 배치하여
# 웹소켓 연결 시 사용자 인증을 수행하도록 합니다.
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack # 기존 AuthMiddlewareStack을 대체하거나 함께 사용

def JwtAuthMiddlewareStack(inner):
    return ProtocolTypeRouter({
        "websocket": JwtAuthMiddleware(URLRouter(inner)),
        "http": AuthMiddlewareStack(URLRouter(inner)), # HTTP 요청은 기존 AuthMiddlewareStack 사용
        # 다른 프로토콜 타입이 있다면 여기에 추가
    })
