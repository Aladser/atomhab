from django.db import models
from rest_framework.exceptions import ValidationError

from authen_drf.models import User
from config.settings import NULLABLE
from libs.truncate_table_mixin import TruncateTableMixin


# ВРЕМЕННОЙ ИНТЕРВАЛ
class DatePeriod(TruncateTableMixin, models.Model):
    """Временной интервал"""

    name = models.CharField(verbose_name="Название", max_length=30, unique=True)
    interval = models.PositiveIntegerField(verbose_name="Интервал (в секундах)", unique=True)

    class Meta:
        verbose_name = "Интервал рассылки"
        verbose_name_plural = "интервалы рассылки"
        ordering = ("pk",)

    def __str__(self):
        return self.name

# МЕСТОПОЛОЖЕНИЕ
class Location(TruncateTableMixin, models.Model):
    """Местоположение"""

    name = models.CharField(verbose_name="Название", max_length=255, unique=True)
    description = models.TextField(verbose_name="Комментарии", **NULLABLE)

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"
        ordering = ("name",)

    def __str__(self):
        return self.name

# ДЕЙСТВИЕ
class Action(TruncateTableMixin, models.Model):
    """Действие"""

    name = models.CharField(verbose_name="Название", max_length=100, unique=True)
    is_pleasant = models.BooleanField(verbose_name="приятное", default=False)
    description = models.TextField(verbose_name="Объяснение", **NULLABLE)

    class Meta:
        verbose_name = "Действие"
        verbose_name_plural = "Действия"
        ordering = ("pk",)

    def __str__(self):
        return self.name

# ВОЗНАГРАЖДЕНИЕ
class Reward(TruncateTableMixin, models.Model):
    """Вознаграждение"""

    name = models.CharField(verbose_name="Название", max_length=100, unique=True)
    description = models.TextField(verbose_name="Объяснение", **NULLABLE)

    class Meta:
        verbose_name = "Вознаграждение"
        verbose_name_plural = "Вознаграждения"
        ordering = ("name",)

    def __str__(self):
        return self.name

# ПРИВЫЧКА
class Habit(TruncateTableMixin, models.Model):
    """ Привычка. Ее можно сделать и полезной, и приятной """

    author = models.ForeignKey(
        to=User,
        verbose_name="Автор",
        on_delete=models.CASCADE,
        related_name='habits',
    )
    location = models.ForeignKey(
        to=Location,
        verbose_name="Место",
        on_delete=models.CASCADE,
        related_name='habits',
    )
    action = models.ForeignKey(
        to=Action,
        verbose_name="Действие",
        on_delete=models.CASCADE,
        related_name='habits',
    )
    periodicity = models.ForeignKey(
        to=DatePeriod,
        verbose_name="Периодичность",
        on_delete=models.CASCADE,
        related_name='habits',
    )

    time = models.TimeField(verbose_name="Время",auto_now_add=True)
    execution_time = models.PositiveIntegerField(verbose_name="Время выполнения, в секундах", default=120)
    is_publiс = models.BooleanField(verbose_name="Общедоступность", default=False)

    def clean(self):
        # Валидация времени исполнения
        if self.execution_time > 120:
            raise ValidationError("Время выполнения не должно превышать 120 секунд")

    def save(self,*args,force_insert=False,force_update=False,using=None,update_fields=None):
        self.full_clean()
        super().save(*args,force_insert,force_update,using,update_fields)

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        unique_together = ('location', 'action', 'time', 'periodicity', 'execution_time', 'is_publiс')
        ordering = ("pk",)

    def __str__(self):
        return f"{self.action} в {self.time} в {self.location}"

# ПРИЯТНАЯ ПРИВЫЧКА
class PleasantHabit(TruncateTableMixin, models.Model):
    """Приятная привычка"""

    habit = models.OneToOneField(
        to=Habit,
        verbose_name="Привычка",
        on_delete=models.CASCADE,
        related_name='pleasant_habit',
        unique=True
    )

    class Meta:
        verbose_name = "Приятная привычка"
        verbose_name_plural = "Приятные привычки"
        ordering = ("pk",)

    def __str__(self):
        return str(self.habit)

# ПОЛЕЗНАЯ ПРИВЫЧКА
class UsefulHabit(TruncateTableMixin, models.Model):
    """Полезная привычка"""

    habit = models.OneToOneField(
        to=Habit,
        verbose_name="Привычка",
        on_delete=models.CASCADE,
        related_name='userful_habit',
        unique=True
    )
    pleasant_habit = models.ForeignKey(
        to=PleasantHabit,
        verbose_name="Приятная привычка",
        on_delete=models.CASCADE,
        related_name='userful_habits',
        default=None,
        **NULLABLE
    )
    reward = models.ForeignKey(
        to=Reward,
        verbose_name="Вознаграждение",
        on_delete=models.CASCADE,
        related_name='userful_habits',
        default=None,
        **NULLABLE
    )

    def clean(self):
        # Валидация указания вознаграждения: полезная привычка или вознаграждение
        if self.pleasant_habit is None and self.reward is None or self.pleasant_habit is not None and self.reward is not None:
            raise ValidationError("Должна быть заполнена связанная приятная привычка или вознаграждение, но не одновременно")

    def save(self,*args,force_insert=False,force_update=False,using=None,update_fields=None):
        self.full_clean()
        super().save(*args,force_insert,force_update,using,update_fields)

    class Meta:
        verbose_name = "Полезная привычка"
        verbose_name_plural = "Полезные привычки"
        unique_together = ('habit','pleasant_habit', 'reward')
        ordering = ("pk",)

    def __str__(self):
        if self.pleasant_habit is None:
            return f"{str(self.habit)} (награда - {self.reward})"
        else:
            return f"{str(self.habit)} (награда - {self.pleasant_habit.name})"

# ПОЛЬЗОВАТЕЛЬСКАЯ ПОЛЕЗНАЯ ПРИВЫЧКА
class UserUsefulHabit(TruncateTableMixin, models.Model):
    """Пользовательская приятная привычка"""

    user = models.ForeignKey(
        to=User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        related_name='user_useful_habits',
    )

    useful_habit = models.ForeignKey(
        to=UsefulHabit,
        verbose_name="Полезная привычка",
        on_delete=models.CASCADE,
        related_name='user_useful_habits',
    )

    class Meta:
        verbose_name = "Пользовательская приятная привычка"
        verbose_name_plural = "Пользовательская приятные привычки"
        ordering = ("pk",)

    def __str__(self):
        return str(self.habit)
