
class OwnerHabitQuerysetMixin:
    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        else:
            queryset = super().get_queryset()
            q1 = queryset.filter(author=self.request.user)
            q2 = queryset.filter(is_publiс=True)
            return q1.union(q2)

