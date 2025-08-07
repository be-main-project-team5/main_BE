from rest_framework import permissions
from rest_framework.permissions import BasePermission


# 어드민의 권한
class IsAdminUser(permissions, BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "ADMIN"
        )


# 아이돌의 권한
class IsIdolUser(permissions, BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "IDOL"
        )


# 매니저의 권한
class IsManagerUser(permissions, BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "MANAGER"
        )


# 아이돌 또는 매니저의 권한
class IsIdolOrManagerUser(permissions, BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (request.user.role == "IDOL" or request.user.role == "MANAGER")
        )
