from rest_framework.permissions import IsAuthenticated

from authen_drf.permissions import IsAuthorPermission

class AuthorPermMixin:
    """Проверка разрешений автороства"""

    def get_permissions(self):
        if self.action != 'list':
            self.permission_classes = [IsAuthenticated, IsAuthorPermission]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
