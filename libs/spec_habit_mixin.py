from rest_framework.permissions import IsAuthenticated

from authen_drf.permissions import IsOwnerPermission


class SpecHabitMixin:
    """Методы для контроллеров полезных и приятных привячек"""
    
    def get_permissions(self):
        if self.action in ['detail', 'update', 'partial_update', 'delete']:
            self.permission_classes = [IsOwnerPermission]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset if self.request.user.is_superuser else queryset.filter(user=self.request.user)
