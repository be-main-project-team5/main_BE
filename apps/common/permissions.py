from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsManagerOrAdminOrReadOnly(BasePermission):
    """
    GET, HEAD, OPTIONS 요청은 모든 사용자에게 허용합니다.
    그 외의 요청(POST, PUT, PATCH, DELETE)은 관리자(is_staff) 또는 매니저(role='MANAGER')에게만 허용합니다.
    """

    def has_permission(self, request, view):
        # 읽기 전용 요청은 항상 허용
        if request.method in SAFE_METHODS:
            return True

        # 쓰기 요청은 인증된 사용자이면서 관리자 또는 매니저일 경우에만 허용
        return (
            request.user
            and request.user.is_authenticated
            and (request.user.is_staff or request.user.role == "MANAGER")
        )
