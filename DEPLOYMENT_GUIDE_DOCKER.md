# 프로젝트 배포 가이드 (AWS EC2 + Docker Compose)

이 문서는 AWS EC2 인스턴스에 Docker Compose를 사용하여 Django 프로젝트를 배포하는 과정을 안내합니다. 프로젝트에 포함된 `Dockerfile`과 `docker-compose.yml`을 활용하여 간단하고 재현 가능성이 높은 배포를 지향합니다.

---

### **1단계: AWS EC2 인스턴스 생성하기**

1.  **AWS EC2 대시보드**로 이동하여 "인스턴스 시작"을 클릭합니다.
2.  **세부 설정**:
    *   **이름**: 원하는 인스턴스 이름을 지정합니다. (예: `main-project-server`)
    *   **AMI (OS 이미지)**: `Ubuntu Server 22.04 LTS` 또는 `Amazon Linux 2023`을 선택합니다.
    *   **인스턴스 유형**: `t2.micro` (프리티어)를 선택합니다.
    *   **키 페어**: 기존 키 페어를 사용하거나 새 키 페어를 생성하고, `.pem` 파일을 다운로드하여 안전한 곳에 보관합니다. 이 파일은 서버 접속 시 유일한 열쇠입니다.
3.  **네트워크 설정 (보안 그룹)**:
    *   "새 보안 그룹 생성"을 선택하고 아래와 같이 **인바운드 규칙**을 설정합니다.
    *   `SSH` (포트 22): 소스를 `내 IP`로 설정하여 자신의 컴퓨터에서만 접속할 수 있도록 제한합니다. (보안 강화)
    *   `HTTP` (포트 80): 소스를 `위치 무관 (0.0.0.0/0)`으로 설정하여 웹 접근을 허용합니다.
    *   `HTTPS` (포트 443): 소스를 `위치 무관 (0.0.0.0/0)`으로 설정하여 보안 웹 접근을 허용합니다.
    *   `사용자 지정 TCP` (포트 8000): 소스를 `위치 무관 (0.0.0.0/0)`으로 설정합니다. (배포 초기 단계에서 Django 서버로 직접 접속하여 테스트하기 위함)
4.  **스토리지 및 고급 세부 정보**: 기본 설정을 유지합니다.
5.  **인스턴스 시작**: 모든 설정을 확인하고 인스턴스를 시작합니다.

---

### **2단계: SSH 접속 및 서버 초기 설정**

> **핵심:** 이 단계에서는 EC2 서버에 **Docker**와 **Git**만 설치합니다. Python, Poetry, 각종 라이브러리 등은 모두 Docker 컨테이너 안에서 관리되므로 서버를 매우 깔끔하게 유지할 수 있습니다.

1.  **SSH로 EC2 인스턴스에 접속**:
    *   터미널을 열고 다운로드한 `.pem` 키 파일의 권한을 변경합니다. (최초 한 번만)
        ```bash
        chmod 400 /path/to/your-key.pem
        ```
    *   SSH 명령어로 서버에 접속합니다.
        ```bash
        ssh -i /path/to/your-key.pem ubuntu@<EC2_PUBLIC_IP_ADDRESS>
        ```

2.  **서버 업데이트 및 필수 패키지 설치**:
    *   서버의 패키지 목록을 최신화하고 시스템을 업그레이드합니다.
        ```bash
        sudo apt-get update && sudo apt-get upgrade -y
        ```
    *   Git, Docker, Docker Compose를 설치합니다.
        ```bash
        # Git 설치 (소스 코드 다운로드용)
        sudo apt-get install git -y

        # Docker 설치 및 서비스 등록
        sudo apt-get install docker.io -y
        sudo systemctl start docker
        sudo systemctl enable docker

        # Docker를 sudo 없이 사용하도록 설정 (권장)
        sudo usermod -aG docker $USER
        
        # Docker Compose 설치
        sudo apt-get install docker-compose -y
        ```
    *   **중요**: `usermod` 명령어 적용을 위해 **SSH 접속을 종료했다가 다시 접속**해야 합니다.

---

### **3단계: 프로젝트 클론 및 환경변수 설정**

1.  **Github Repository 클론**:
    *   Git을 이용해 프로젝트 소스 코드를 서버로 가져옵니다.
        ```bash
        git clone <YOUR_GITHUB_REPOSITORY_URL>
        ```
    *   생성된 프로젝트 디렉터리로 이동합니다.
        ```bash
        cd main_BE
        ```

2.  **환경변수 파일 `.env` 생성**:
    *   `docker-compose.yml`이 참조할 `.env` 파일을 생성하고 편집합니다.
        ```bash
        nano .env
        ```
    *   편집기가 열리면 아래 내용을 **자신의 환경에 맞게 수정**하여 입력합니다.
        ```env
        # Django Secret Key (보안을 위해 새로운 키를 생성하여 사용하세요)
        # 로컬에서 `python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` 명령어로 생성 가능
        SECRET_KEY=your_strong_secret_key_here

        # 데이터베이스 설정 (docker-compose.yml의 db 서비스와 연동)
        DB_NAME=main_db
        DB_USER=main_user
        DB_PASSWORD=a_very_strong_and_secret_password

        # 포트 번호
        DB_PORT=5432
        ```
    *   작성이 끝나면 `Ctrl+X` -> `Y` -> `Enter`를 눌러 저장합니다.

---

### **4단계: Docker Compose로 애플리케이션 실행**

아래 명령어 한 줄로 `docker-compose.yml`에 정의된 모든 서비스(web, db, redis)가 빌드되고 실행됩니다.

1.  **Docker 이미지 빌드 및 컨테이너 실행**:
    ```bash
    docker-compose up --build -d
    ```
    *   `up`: 서비스를 시작합니다.
    *   `--build`: `Dockerfile`이 변경되었거나 처음 실행할 때 이미지를 새로 만듭니다.
    *   `-d`: 백그라운드에서 실행하여 터미널을 계속 사용할 수 있게 합니다.

2.  **컨테이너 상태 확인**:
    *   서비스들이 정상적으로 실행 중인지 확인합니다.
        ```bash
        docker-compose ps
        ```
    *   `main_be_web`, `main_be_db`, `main_be_redis` 컨테이너의 `State`가 모두 `Up`으로 표시되어야 합니다.

3.  **데이터베이스 마이그레이션 및 관리자 생성**:
    *   `docker-compose exec` 명령어를 사용하여 실행 중인 `web` 컨테이너 내부에서 `manage.py` 명령을 실행합니다.
        ```bash
        # 데이터베이스 테이블 생성 (마이그레이션)
        docker-compose exec web python manage.py migrate

        # 관리자 계정 생성
        docker-compose exec web python manage.py createsuperuser
        ```

---

### **5단계: 접속 테스트**

*   웹 브라우저의 주소창에 `http://<EC2_PUBLIC_IP_ADDRESS>:8000`을 입력하여 접속합니다.
*   Django 웰컴 페이지 또는 DRF API 문서 페이지가 나타나면 성공적으로 배포된 것입니다.

---

### **다음 단계: 프로덕션을 위한 준비**

현재 상태는 외부에서 접속 가능한 개발 서버입니다. 실제 서비스를 운영하기 위해서는 아래 과정들을 추가하는 것이 좋습니다.

1.  **Nginx 리버스 프록시 도입**:
    *   `docker-compose.yml`에 Nginx 서비스를 추가합니다.
    *   사용자의 요청(80, 443 포트)을 Nginx가 먼저 받은 후, 내부적으로 Django `web` 컨테이너(8000 포트)로 전달하도록 구성합니다.
    *   정적 파일(Static files) 서빙을 Nginx가 담당하도록 하여 Django의 부하를 줄입니다.
2.  **도메인 연결**:
    *   `Route 53`과 같은 DNS 서비스에서 도메인을 구입하고, EC2 인스턴스의 고정 IP(Elastic IP)에 연결합니다.
3.  **HTTPS 적용 (SSL 인증서)**:
    *   Nginx 컨테이너에 `Certbot`을 설치하여 Let's Encrypt의 무료 SSL 인증서를 발급받고, `https://` 보안 연결을 설정합니다.
