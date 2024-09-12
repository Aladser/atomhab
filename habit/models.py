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
    """Привычка. Ее можно сделать и полезной, и приятной"""

    location = models.ForeignKey(
        to=Place,
        verbose_name="Место",
        on_delete=models.CASCADE,
        related_name='habits',
    )
    action = models.ForeignKey(
        to=Action,
        verbose_name="Действие",
        on_delete=models.CASCADE,
        related_name='habits'
    )
    time = models.TimeField(verbose_name="Время",auto_now=True)

    periodicity = models.ForeignKey(
        to=DatePeriod,
        verbose_name="Периодичность",
        on_delete=models.CASCADE,
        related_name='habits'
    )
    execution_time = models.PositiveIntegerField(verbose_name="Время выполнения, в секундах",default=120)
    is_publiс = models.BooleanField(verbose_name="Общедоступный",default=False)

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        unique_together = ('location', 'action', 'time')
        ordering = ("-pk",)

    def __str__(self):
        return f"{self.action} в {self.time} в {self.location}"


class UsefulHabit(TruncateTableMixin, models.Model):
    """Полезная привычка"""

    pleasant_habit = models.ForeignKey(
        to=Habit,
        verbose_name="Приятная привычка",
        on_delete=models.CASCADE,
        related_name='useful_habits',
        default=None,
        **NULLABLE,
    )
    reward = models.ForeignKey(
        to=Reward,
        verbose_name="Вознаграждение",
        on_delete=models.CASCADE,
        related_name='useful_habits',
        default=None,
        **NULLABLE
    )

class UserUsefulHabit(TruncateTableMixin, models.Model):
    """Пользовательская полезная привычка"""

    user = models.ForeignKey(
        to=User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        related_name='userful_habits',
        **NULLABLE
    )
    habit = models.ForeignKey(
        to=UsefulHabit,
        verbose_name="Полезная привычка",
        on_delete=models.CASCADE,
        related_name='userful_habits',
        **NULLABLE
    )

class UserPleasantHabit(TruncateTableMixin, models.Model):
    """Пользовательская приятная привычка"""

    user = models.ForeignKey(
        to=User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        related_name='user_pleasant_habits',
        **NULLABLE
    )
    habit = models.ForeignKey(
        to=Habit,
        verbose_name="Приятная привычка",
        on_delete=models.CASCADE,
        related_name='user_pleasant_habits',
        **NULLABLE
    )

