from rest_framework import permissions
from rest_framework.permissions import BasePermission
from apps.idols.models import IdolManager # IdolManager 모델 임포트


# 어드민의 권한
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "ADMIN"
        )


# 아이돌의 권한
class IsIdolUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "IDOL"
        )


# 매니저의 권한
class IsManagerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "MANAGER"
        )


# 아이돌 또는 매니저의 권한
class IsIdolOrManagerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (request.user.role == "IDOL" or request.user.role == "MANAGER")
        )


# 매니저 또는 관리자의 권한
class IsManagerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        # 읽기 권한은 모든 사용자에게 허용
        if request.method in permissions.SAFE_METHODS:
            return True
        # 쓰기 권한은 매니저 또는 관리자에게만 허용
        return request.user and request.user.is_authenticated and \
               (request.user.role == 'MANAGER' or request.user.role == 'ADMIN')

    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 모든 사용자에게 허용
        if request.method in permissions.SAFE_METHODS:
            return True

        # 객체 수정/삭제 권한은 매니저 또는 관리자에게만 허용
        if request.user.role == 'ADMIN':
            return True
        elif request.user.role == 'MANAGER':
            # 매니저는 자신이 담당하는 아이돌의 스케줄만 수정/삭제 가능
            # obj는 IdolSchedule 인스턴스
            return IdolManager.objects.filter(user=request.user, idol=obj.idol).exists()
        return False
