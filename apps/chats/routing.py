from django.urls import re_path

from . import consumers

# websocket_urlpatterns: 웹소켓 연결 요청이 들어왔을 때, URL 패턴에 따라 어떤 Consumer가 처리할지 정의합니다.
# 연동: config/asgi.py에서 URLRouter를 통해 이 패턴들을 로드하여 웹소켓 요청을 처리합니다.
websocket_urlpatterns = [
    # re_path: 정규 표현식을 사용하여 URL 패턴을 정의합니다.
    # r"ws/chats/(?P<room_name>\w+)/$":
    #   - ws/chats/: 웹소켓 URL의 시작 부분입니다.
    #   - (?P<room_name>\w+): URL 경로에서 'room_name'이라는 이름으로 값을 추출합니다.
    #     \w+: 단어 문자(알파벳, 숫자, 언더스코어) 하나 이상을 의미합니다.
    #   - /: 슬래시로 끝납니다.
    #   - $: 문자열의 끝을 의미합니다.
    # consumers.ChatConsumer.as_asgi(): 이 패턴에 매칭되는 웹소켓 요청이 들어오면 ChatConsumer를 ASGI 애플리케이션으로 실행합니다.
    re_path(r"ws/chats/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]
