from django.db import models
from rest_framework.exceptions import ValidationError

from authen_drf.models import User
from config.settings import NULLABLE
from libs.manual_model_saving_mixin import ManualModelSavingMixin
from libs.truncate_table_mixin import TruncateTableMixin


# ПЕРИОДИЧНОСТЬ
class Periodicity(TruncateTableMixin, models.Model):
    """Периодичность"""

    name = models.CharField(verbose_name="Название", max_length=30, unique=True)
    interval = models.PositiveIntegerField(verbose_name="Интервал (в секундах)", unique=True)

    class Meta:
        verbose_name = "Периодичность"
        verbose_name_plural = "Периодичности"
        ordering = ("pk",)

    def clean(self):
        print(self.interval)
        # Валидация периодичности - не больше 1 недели
        if self.interval > 60*60*24*7:
            raise ValidationError("Интервал периодичности не должен превышать одну неделю")

    def save(self,*args,force_insert=False,force_update=False,using=None,update_fields=None):
        self.full_clean()
        super().save(*args,force_insert,force_update,using,update_fields)

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

    name = models.CharField(verbose_name="Название", max_length=100)
    is_pleasant = models.BooleanField(verbose_name="Приятное", default=False)
    description = models.TextField(verbose_name="Объяснение", **NULLABLE)

    class Meta:
        verbose_name = "Действие"
        verbose_name_plural = "Действия"
        ordering = ("pk",)
        unique_together = ('name', 'is_pleasant')

    def __str__(self):
        return f"Приятно {self.name}" if self.is_pleasant else f"Полезно {self.name}"

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
class Habit(TruncateTableMixin, ManualModelSavingMixin, models.Model):
    """ Привычка """

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
        to=Periodicity,
        verbose_name="Периодичность",
        on_delete=models.CASCADE,
        related_name='habits',
    )

    time = models.TimeField(verbose_name="Время")
    execution_time = models.PositiveIntegerField(verbose_name="Время выполнения, в секундах", default=120)
    is_publiс = models.BooleanField(verbose_name="Общедоступность", default=False)

    def clean(self):
        # Валидация времени исполнения
        if self.execution_time > 120:
            raise ValidationError("Время выполнения не должно превышать 120 секунд")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        unique_together = ('location', 'action', 'time')
        ordering = ("pk",)

    def __str__(self):
        return f"{self.action} в {str(self.time)[:8]} в {self.location}"

# ПРИЯТНАЯ ПРИВЫЧКА
class PleasantHabit(TruncateTableMixin, ManualModelSavingMixin, models.Model):
    """Приятная привычка"""
    user = models.ForeignKey(
        to=User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        related_name='pleasant_habits',
    )
    habit = models.ForeignKey(
        to=Habit,
        verbose_name="Привычка",
        on_delete=models.CASCADE,
        related_name='pleasant_habits',
        **NULLABLE
    )

    class Meta:
        verbose_name = "Приятная привычка"
        verbose_name_plural = "Приятные привычки"
        ordering = ("pk",)
        unique_together = ('user', 'habit')

    def clean(self):
        # Валидация приятного действия
        if not self.habit.action.is_pleasant:
            raise ValidationError("Действие привычки не является приятным")
        # Валидация разрешения пользователя использовать указанную привычку
        if not self.user.is_superuser and self.habit.author != self.user and not self.habit.is_publiс:
            raise ValidationError("Вы не можете использовать эту приятную привычку, так как не являетесь автором, и привычка не общем доступе")

    def __str__(self):
        return self.habit

# ПОЛЕЗНАЯ ПРИВЫЧКА
class UsefulHabit(TruncateTableMixin, ManualModelSavingMixin, models.Model):
    """Полезная привычка"""
    user = models.ForeignKey(
        to=User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        related_name='userful_habits',
    )
    habit = models.ForeignKey(
        to=Habit,
        verbose_name="Привычка",
        on_delete=models.CASCADE,
        related_name='userful_habits',
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
        # Валидация полезного действия
        if self.habit.action.is_pleasant:
            raise ValidationError("Действие привычки не является полезным")
        # Валидация указанного вознаграждения: полезная привычка или вознаграждение
        if self.pleasant_habit is None and self.reward is None or self.pleasant_habit is not None and self.reward is not None:
            raise ValidationError("Должна быть заполнена связанная приятная привычка или вознаграждение, но не одновременно")
        # Валидация разрешения пользователя использовать указанную привычку
        if not self.user.is_superuser and self.habit.author != self.user and not self.habit.is_publiс:
                raise ValidationError("Вы не можете использовать эту полезную привычку, так как не являетесь автором, и привычка не общем доступе")

    class Meta:
        verbose_name = "Полезная привычка"
        verbose_name_plural = "Полезные привычки"
        ordering = ("pk",)
        unique_together = ('user', 'habit')

    def __str__(self):
        if self.pleasant_habit is None:
            return f"{self.habit} (награда - {self.reward})"
        else:
            return f"{self.habit} (награда - {self.pleasant_habit.name})"

