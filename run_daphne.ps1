# run_daphne.ps1

# 가상 환경 활성화 (필요시 주석 해제)
# .\venv\Scripts\Activate.ps1

# Django 설정 모듈 환경 변수 설정
$env:DJANGO_SETTINGS_MODULE="config.settings"

# Daphne 서버 실행
daphne config.asgi:application
