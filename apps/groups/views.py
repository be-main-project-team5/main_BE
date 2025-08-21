from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets

from apps.common.permissions import IsManagerOrAdminOrReadOnly

from .models import Group
from .serializers import GroupSerializer


# Django REST Framework의 ViewSet을 사용하여 Group 모델에 대한 API 엔드포인트를 제공합니다.
# ModelViewSet을 상속받아 기본적인 CRUD(Create, Retrieve, Update, Delete) 작업을 위한
# 리스트(GET), 상세 조회(GET), 생성(POST), 업데이트(PUT/PATCH), 삭제(DELETE) 기능을 자동으로 구현합니다.
# 이 ViewSet은 'apps/groups/urls.py'에서 URL 라우터에 등록되어 실제 API 엔드포인트를 생성합니다.
@extend_schema_view(
    list=extend_schema(
        tags=["아이돌 그룹 (Groups)"],
        summary="아이돌 그룹 목록 조회",
        description="모든 아이돌 그룹의 목록을 조회합니다."
    ),
    retrieve=extend_schema(
        tags=["아이돌 그룹 (Groups)"],
        summary="아이돌 그룹 상세 조회",
        description="특정 아이돌 그룹의 상세 정보를 조회합니다."
    ),
    create=extend_schema(
        tags=["아이돌 그룹 (Groups)"],
        summary="아이돌 그룹 생성",
        description="새로운 아이돌 그룹을 생성합니다. 매니저 또는 관리자만 가능합니다."
    ),
    update=extend_schema(
        tags=["아이돌 그룹 (Groups)"],
        summary="아이돌 그룹 정보 수정",
        description="기존 아이돌 그룹의 정보를 수정합니다. 해당 그룹의 매니저 또는 관리자만 가능합니다."
    ),
    partial_update=extend_schema(
        tags=["아이돌 그룹 (Groups)"],
        summary="아이돌 그룹 정보 부분 수정",
        description="기존 아이돌 그룹의 정보 일부를 수정합니다. 해당 그룹의 매니저 또는 관리자만 가능합니다."
    ),
    destroy=extend_schema(
        tags=["아이돌 그룹 (Groups)"],
        summary="아이돌 그룹 삭제",
        description="아이돌 그룹을 삭제합니다. 해당 그룹의 매니저 또는 관리자만 가능합니다."
    )
)
class GroupViewSet(viewsets.ModelViewSet):
    # 이 ViewSet이 다룰 모델 인스턴스들의 쿼리셋을 정의합니다.
    # Group.objects.all()은 데이터베이스에서 모든 Group 객체를 가져오도록 지시합니다.
    # 이 쿼리셋은 API 요청(예: GET /api/v1/groups/)이 들어왔을 때 데이터를 조회하는 데 사용됩니다.
    queryset = Group.objects.all()

    # 이 ViewSet에서 데이터를 직렬화하고 역직렬화하는 데 사용할 시리얼라이저 클래스를 정의합니다.
    # 'apps/groups/serializers.py'에 정의된 GroupSerializer를 사용하여
    # Python 객체(Group 모델 인스턴스)를 JSON과 같은 웹 친화적인 형식으로 변환하거나 그 반대로 변환합니다.
    serializer_class = GroupSerializer

    permission_classes = [IsManagerOrAdminOrReadOnly]
