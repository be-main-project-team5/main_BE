# 1. 기본 이미지 설정 (Python 3.13 슬림 버전)
FROM python:3.13-slim

# 2. 환경 변수 설정
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 3. 작업 디렉터리 설정
WORKDIR /app

# 4. 소스 코드 및 설정 파일 복사
COPY . .

# 5. 의존성 설치
#    - pip을 최신 버전으로 업그레이드하고, pyproject.toml을 이용해 의존성을 설치합니다.
RUN pip install --upgrade pip && \
    pip install .

# 6. 포트 노출
EXPOSE 8000

# 7. Gunicorn 서버 실행
CMD ["gunicorn", "config.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "-w", "4", "-b", "0.0.0.0:8000"]
