import os
import sys

# DJANGO_SETTINGS_MODULE 환경 변수 값을 가져옵니다.
# 만약 설정되지 않았다면, 기본값으로 'config.settings.dev'를 사용합니다.
# config는 startproject 시 생성한 프로젝트 이름입니다.
settings_module_name = os.environ.get("DJANGO_SETTINGS_MODULE", "config.settings.dev")

# 설정 모듈 이름에서 마지막 부분(dev, prod 등)을 추출합니다.
# 예: 'config.settings.dev' -> 'dev'
# 'config.settings.prod' -> 'prod'
env = settings_module_name.split(".")[-1]

if env == "prod":
    from .prod import *
elif env == "dev":
    from .dev import *
else:
    # 예상치 못한 DJANGO_SETTINGS_MODULE 값일 경우 오류 처리
    sys.stderr.write(
        f"Error: Invalid DJANGO_SETTINGS_MODULE value '{settings_module_name}'. "
        f"Expected 'config.settings.dev' or 'config.settings.prod'.\n"
    )
    sys.exit(1)
