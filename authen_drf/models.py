from django.contrib.auth.models import AbstractUser
from django.db import models

from config.settings import NULLABLE
from libs.truncate_table_mixin import TruncateTableMixin


# -----ПОЛЬЗОВАТЕЛЬ-----
class User(TruncateTableMixin, AbstractUser):
    username = None
    email = models.EmailField(verbose_name='почта', unique=True)
    tg_chat_id = models.CharField(verbose_name="ID телеграм чата", **NULLABLE, max_length=100)

    phone = models.CharField(verbose_name='телефон', unique=True, max_length=20, **NULLABLE)
    avatar = models.ImageField(verbose_name='аватар', upload_to='images/users', **NULLABLE)
    token = models.CharField(verbose_name="токен", **NULLABLE, max_length=100)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('first_name', 'last_name', 'email')

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else self.email
