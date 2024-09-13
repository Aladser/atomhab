from authen_drf.permissions import IsAuthorPermission


class AuthorViewsetMixin:
    """Миксин, вызывающий методыб учитывая авторизованного пользователя """

    def get_permissions(self):
        if self.action in ['detail', 'update', 'partial_update', 'delete']:
            self.permission_classes = [IsAuthorPermission]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        request.data['author'] = request.user.pk
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset if self.request.user.is_superuser else queryset.filter(author=self.request.user)
