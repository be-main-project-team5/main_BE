# 1. 기본 이미지 설정 (Python 3.13 슬림 버전)
FROM python:3.13-slim

# 2. 환경 변수 설정
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 3. 작업 디렉터리 설정
WORKDIR /app

# 4. 의존성 설치
#    - 먼저 pyproject.toml 파일을 복사합니다.
COPY pyproject.toml ./

#    - pip을 최신 버전으로 업그레이드하고, pyproject.toml을 이용해 의존성을 설치합니다.
#    - 이 방법은 rye를 Dockerfile 내에서 설치할 필요가 없어 더 안정적이고 표준적입니다.
RUN pip install --upgrade pip && \
    pip install .

# 5. 소스 코드 복사
#    - 나머지 소스 코드를 복사합니다.
COPY . .

# 6. 포트 노출
EXPOSE 8000

# 7. Gunicorn 서버 실행
CMD ["gunicorn", "config.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "-w", "4", "-b", "0.0.0.0:8000"]