import json
import time

import websocket

# 이 스크립트는 Django Channels 서버와 웹소켓 통신을 테스트하기 위한 클라이언트입니다.

# --- 설정 --- #
# 실제 채팅방 ID로 변경해야 합니다.
# 이 ID는 Django REST API를 통해 채팅방을 생성했을 때 반환되는 ID입니다.
room_id = 1

# 웹소켓 서버의 URL을 정의합니다.
# Django Channels의 라우팅 설정(apps/chats/routing.py)과 일치해야 합니다.
ws_url = f"ws://127.0.0.1:8000/ws/chats/{room_id}/"

# --- 웹소켓 이벤트 핸들러 --- #


# on_message: 웹소켓 서버로부터 메시지를 수신했을 때 호출됩니다.
# ws: 웹소켓 클라이언트 인스턴스
# message: 수신된 메시지 내용 (문자열)
def on_message(ws, message):
    print(f"Received: {message}")


# on_error: 웹소켓 통신 중 오류가 발생했을 때 호출됩니다.
# ws: 웹소켓 클라이언트 인스턴스
# error: 발생한 오류 객체
def on_error(ws, error):
    print(f"Error: {error}")


# on_close: 웹소켓 연결이 닫혔을 때 호출됩니다.
# ws: 웹소켓 클라이언트 인스턴스
# close_status_code: 연결 종료 상태 코드
# close_msg: 연결 종료 메시지
def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


# on_open: 웹소켓 연결이 성공적으로 열렸을 때 호출됩니다.
# ws: 웹소켓 클라이언트 인스턴스
def on_open(ws):
    print("### opened ###")
    # 연결 후 서버로 메시지를 보냅니다.
    message_content = "Python 스크립트에서 보낸 메시지입니다!"
    # 메시지 내용을 JSON 형식으로 변환하여 보냅니다.
    ws.send(json.dumps({"message": message_content}))
    print(f"Sent: {message_content}")
    # 메시지를 보낸 후 바로 연결을 닫으려면 아래 주석을 해제하세요.
    # ws.close()


# --- 스크립트 실행 진입점 --- #

if __name__ == "__main__":
    # websocket.enableTrace(True): 웹소켓 통신 과정을 콘솔에 자세히 출력하여 디버깅에 도움을 줍니다.
    # (선택 사항이며, 필요 없으면 주석 처리하거나 삭제할 수 있습니다.)
    websocket.enableTrace(True)

    # WebSocketApp 인스턴스를 생성합니다.
    # ws_url: 연결할 웹소켓 서버 주소
    # on_open, on_message, on_error, on_close: 각 이벤트 발생 시 호출될 핸들러 함수들
    ws = websocket.WebSocketApp(
        ws_url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    # 웹소켓 연결을 시작하고 유지합니다.
    # run_forever(): 연결이 닫히거나 오류가 발생하기 전까지 계속 실행됩니다.
    # 메시지를 한 번만 보내고 종료하려면 on_open에서 ws.close()를 호출하거나,
    # run_forever() 대신 다른 방식으로 연결을 관리해야 합니다.
    ws.run_forever()
