from django.db import models

from authen_drf.models import User
from config.settings import NULLABLE
from libs.truncate_table_mixin import TruncateTableMixin

class DatePeriod(models.Model):
    """Временной интервал"""

    name = models.CharField(verbose_name="Название", max_length=30)
    interval = models.PositiveIntegerField(verbose_name="Интервал (в секундах)")

    class Meta:
        verbose_name = "Интервал рассылки"
        verbose_name_plural = "интервалы рассылки"
        ordering = ("pk",)

    def __str__(self):
        return self.name


class Place(TruncateTableMixin, models.Model):
    """Место"""

    name = models.CharField(verbose_name="Название", max_length=255)
    description = models.TextField(verbose_name="Комментарии", **NULLABLE)

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"
        ordering = ("pk",)

    def __str__(self):
        return self.name


class Action(TruncateTableMixin, models.Model):
    """Действие"""

    name = models.CharField(verbose_name="Название", max_length=100)
    description = models.TextField(verbose_name="Объяснение", **NULLABLE)

    class Meta:
        verbose_name = "Действие"
        verbose_name_plural = "Действия"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Reward(TruncateTableMixin, models.Model):
    """Вознаграждение"""

    name = models.CharField(verbose_name="Название", max_length=100)
    description = models.TextField(verbose_name="Объяснение", **NULLABLE)

    class Meta:
        verbose_name = "Вознаграждение"
        verbose_name_plural = "Вознаграждения"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Habit(TruncateTableMixin, models.Model):
    """Привычка"""

    user = models.ForeignKey(
        to=User,
        verbose_name="Создатель",
        on_delete=models.CASCADE,
        related_name='habits'
    )
    place = models.ForeignKey(
        to=Place,
        verbose_name="Место",
        on_delete=models.CASCADE,
        related_name='habits',
    )
    datetime = models.DateTimeField(verbose_name="Время",auto_now=True)
    action = models.ForeignKey(
        to=Action,
        verbose_name="Действие",
        on_delete=models.CASCADE,
        related_name='habits'
    )

    is_pleasant = models.BooleanField(verbose_name="Признак приятной привычки",default=False)
    interval = models.ForeignKey(
        to=DatePeriod,
        verbose_name="Периодичность",
        on_delete=models.CASCADE,
        related_name='habits'
    )
    reward = models.ForeignKey(
        to=Reward,
        verbose_name="Вознаграждение",
        on_delete=models.CASCADE,
        related_name='habits',
        **NULLABLE
    )
    execution_time = models.PositiveIntegerField(verbose_name="Время выполнения, в секундах",default=120)
    is_published = models.BooleanField(verbose_name="Признак публикации",default=False)

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ("-pk",)

    def __str__(self):
        return f"Пользователь {self.user} будет {self.action} в {self.datetime} в {self.place}"


class RelatedHabit(TruncateTableMixin, models.Model):
    """Связанная привычка"""

    related_link = models.ForeignKey(
        to=Habit,
        verbose_name="привычка",
        on_delete=models.CASCADE,
        related_name='related_habits'
    )

    class Meta:
        verbose_name = "Связанная привычка"
        verbose_name_plural = "Связанные привычки"
        ordering = ("-pk",)

    def __str__(self):
        return f"{self.pk} - {self.related_link}"

