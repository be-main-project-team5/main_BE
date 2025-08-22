FROM python:3.13-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install uv

COPY pyproject.toml uv.lock ./

# 가상 환경에 의존성 설치
RUN uv sync --frozen

# Final Stage
FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    # 표준 출력(stdout)과 표준 에러(stderr) 스트림을 실시간으로 표시
    PYTHONDONTWRITEBYTECODE=1
    # .pyc 파일(바이트코드 캐시 파일)을 생성하지 않도록 설정 / 이미지 크기 최적화

# 작업 디렉토리 설정
WORKDIR /app

# 런타임에 필요한 시스템 의존성만 설치 (용량이 작은 libpq5 사용), health check용 curl 설치
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Builder 스테이지에서 생성한 가상환경을 통째로 복사
COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

# 나머지 소스 코드를 복사
COPY . .

# 포트 노출
EXPOSE 8000

RUN chmod +x ./resources/scripts/run.sh

# 서버 실행
CMD ["bash", "resources/scripts/run.sh"]