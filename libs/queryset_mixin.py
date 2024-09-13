class AuthorQuerysetMixin:
    """Доступ к списку своих или всех элементов модели"""

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        else:
            return super().get_queryset().filter(author=self.request.user)
