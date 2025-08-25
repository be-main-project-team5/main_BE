from urllib.parse import parse_qs

import jwt
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from channels.security.websocket import AllowedHostsOriginValidator
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

User = get_user_model()


@database_sync_to_async
def get_user_from_token(token: str):
    try:
        # JWT 디코딩
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"],  # JWT 발급 시 사용한 알고리즘과 동일해야 함
        )
        user_id = payload.get("user_id")  # JWT payload 안의 user_id
        if not user_id:
            return AnonymousUser()

        return User.objects.get(id=user_id)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    """
    쿼리 파라미터에서 `?token=xxx` 로 전달된 JWT를 인증하여
    scope["user"] 에 유저 객체를 세팅하는 미들웨어
    """

    async def __call__(self, scope, receive, send):
        # WebSocket 연결 요청 시 쿼리 파라미터 파싱
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token")

        if token:
            scope["user"] = await get_user_from_token(token[0])
        else:
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)


def JWTAuthMiddlewareStack(inner):
    return AllowedHostsOriginValidator(JWTAuthMiddleware(inner))
