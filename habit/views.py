import datetime

from django.core.exceptions import ValidationError
from rest_framework import generics, exceptions
from rest_framework.viewsets import ModelViewSet

from habit.models import Location, Action, Reward, Habit, PleasantHabit, UsefulHabit, Periodicity
from habit.paginators import ManualPagination
from habit.serializers import LocationSerializer, ActionSerializer, RewardSerializer, HabitSerializer, \
    PleasantHabitSerializer, UsefulHabitSerializer, PeriodicitySerializer
from libs.author_viewset_mixin import AuthorViewsetMixin


# ---Периодичность---
class PeriodicityListAPIView(generics.ListAPIView):
    serializer_class = PeriodicitySerializer
    queryset = Periodicity.objects.all()
class PeriodicityCreateAPIView(generics.CreateAPIView):
    serializer_class = PeriodicitySerializer
class PeriodicityDestroyAPIView(generics.DestroyAPIView):
    serializer_class = PeriodicitySerializer
    queryset = Periodicity.objects.all()


# ---Место---
class LocationListAPIView(generics.ListAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
class LocationCreateAPIView(generics.CreateAPIView):
    serializer_class = LocationSerializer
class LocationDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()


# ---Действие---
class ActionListAPIView(generics.ListAPIView):
    serializer_class = ActionSerializer
    queryset = Action.objects.all()
class ActionCreateAPIView(generics.CreateAPIView):
    serializer_class = ActionSerializer
class ActionDestroyAPIView(generics.DestroyAPIView):
    serializer_class = ActionSerializer
    queryset = Action.objects.all()


# ---Вознаграждение---
class RewardListAPIView(generics.ListAPIView):
    serializer_class = RewardSerializer
    queryset = Reward.objects.all()
class RewardCreateAPIView(generics.CreateAPIView):
    serializer_class = RewardSerializer
class RewardDestroyAPIView(generics.DestroyAPIView):
    serializer_class = RewardSerializer
    queryset = Reward.objects.all()


# --- Публичные привычки ---
class PublicHabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(is_publiс=True)

# --- Привычка ---
class HabitViewSet(AuthorViewsetMixin, ModelViewSet):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = ManualPagination

    def perform_create(self, serializer):
        habit = serializer.save()
        # округляет время
        habit.time = datetime.time(habit.time.hour, habit.time.minute)
        try:
            habit.save()
        except ValidationError as e:
            raise exceptions.ValidationError(f"Привычка <<{habit}>> уже существует")

# --- Приятная привычка ---
class PleasantHabitViewSet(AuthorViewsetMixin, ModelViewSet):
    serializer_class = PleasantHabitSerializer
    queryset = PleasantHabit.objects.all()
    pagination_class = ManualPagination

# --- Полезная привычка ---
class UsefulHabitViewSet(AuthorViewsetMixin, ModelViewSet):
    serializer_class = UsefulHabitSerializer
    queryset = UsefulHabit.objects.all()
    pagination_class = ManualPagination




