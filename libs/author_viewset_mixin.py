from authen_drf.permissions import IsAuthorPermission


class AuthorViewsetMixin:
    """Миксин, вызывающий методыб учитывая авторизованного пользователя """

    def get_permissions(self):
        if self.action in ['detail', 'update', 'partial_update', 'delete']:
            self.permission_classes = [IsAuthorPermission]
        return super().get_permissions()

    def get_serializer(self, *args, **kwargs):
        if self.action == 'create':
            kwargs['data']['author'] = self.request.user.pk
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        else:
            return super().get_queryset().filter(author=self.request.user)
