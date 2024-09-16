from django.http import QueryDict
from rest_framework.fields import empty


class InitCreateSerializerMixin:
    """Метод init() сериализатороа создания"""

    def __init__(self, instance=None, data=empty, **kwargs):
        if type(data) != QueryDict:
            data['user'] = kwargs['context']['request'].user.pk
        super().__init__(instance, data, **kwargs)
