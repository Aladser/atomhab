from rest_framework import permissions

# проверка создателя объекта
class IsAuthorPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or request.user.is_superuser

class IsSuperUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return False

