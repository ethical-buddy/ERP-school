from rest_framework.permissions import BasePermission


class IsAdminManagerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if getattr(view, "block_student_role", False) and request.user.groups.filter(name="student_portal").exists():
            return False
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        if request.user.is_superuser:
            return True
        return request.user.groups.filter(name__in=["api_admin", "api_manager"]).exists()
