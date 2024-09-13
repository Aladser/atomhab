
class OwnerQuerysetMixin:
    def get_queryset(self):
        if not self.request.user.is_superuser:
            return super().get_queryset().filter(author=self.request.user)
        else:
            return super().get_queryset()
