
class OwnerHabitQuerysetMixin:
    """Доступ к списку своих или всех привычек"""

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        else:
            queryset = super().get_queryset()
            q1 = queryset.filter(author=self.request.user)
            q2 = queryset.filter(is_publiс=True)
            return q1.union(q2)

class OwnerQuerysetMixin:
    """Доступ к списку своих или всех элементов модели"""

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        else:
            return super().get_queryset().filter(author=self.request.user)
