from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminRole(BasePermission):
    """อนุญาตเฉพาะ Role 'ADMIN'"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'ADMIN')

class IsAdminOrAdminLimitedRole(BasePermission):
    """อนุญาต Role 'ADMIN' หรือ 'ADMIN_LIMITED'"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role in ['ADMIN', 'ADMIN_LIMITED'])

class IsAgentRole(BasePermission):
    """อนุญาต Role 'AGENT' และ 'ADMIN'"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role in ['ADMIN', 'ADMIN_LIMITED','AGENT'])

class IsViewerRoleReadOnly(BasePermission):
    """อนุญาตให้ทุกคนที่ Login ดูได้อย่างเดียว (Read-Only)"""
    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS and request.user and request.user.is_authenticated)