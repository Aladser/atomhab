import datetime

from django.db import IntegrityError
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet

from habit.models import Location, Action, Reward, Habit, PleasantHabit, UsefulHabit, Periodicity
from habit.paginators import ManualPagination
from habit.serializers import LocationSerializer, ActionSerializer, RewardSerializer, HabitSerializer, \
    PleasantHabitSerializer, UsefulHabitSerializer, PeriodicitySerializer
from libs.owner_queryset import OwnerHabitQuerysetMixin, OwnerQuerysetMixin


# ---PERIODICITY---
class PeriodicityListAPIView(generics.ListAPIView):
    serializer_class = PeriodicitySerializer
    queryset = Periodicity.objects.all()
class PeriodicityCreateAPIView(generics.CreateAPIView):
    serializer_class = PeriodicitySerializer
class PeriodicityDestroyAPIView(generics.DestroyAPIView):
    serializer_class = PeriodicitySerializer
    queryset = Periodicity.objects.all()

# ---LOCATION---
class LocationListAPIView(generics.ListAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
class LocationCreateAPIView(generics.CreateAPIView):
    serializer_class = LocationSerializer
class LocationDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()


# ---ACTION---
class ActionListAPIView(generics.ListAPIView):
    serializer_class = ActionSerializer
    queryset = Action.objects.all()
class ActionCreateAPIView(generics.CreateAPIView):
    serializer_class = ActionSerializer
class ActionDestroyAPIView(generics.DestroyAPIView):
    serializer_class = ActionSerializer
    queryset = Action.objects.all()


# ---REWARD---
class RewardListAPIView(generics.ListAPIView):
    serializer_class = RewardSerializer
    queryset = Reward.objects.all()
class RewardCreateAPIView(generics.CreateAPIView):
    serializer_class = RewardSerializer
class RewardDestroyAPIView(generics.DestroyAPIView):
    serializer_class = RewardSerializer
    queryset = Reward.objects.all()


# --- HABIT ---
class HabitViewSet(OwnerHabitQuerysetMixin, ModelViewSet):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = ManualPagination

    def perform_create(self, serializer):
        habit = serializer.save()
        # округляет время
        habit.time = datetime.time(habit.time.hour, habit.time.minute)
        try:
            habit.save()
        except IntegrityError as e:
            raise ValidationError(f"<<{str(habit)}>>: дубликат привычки")

# --- PLEASANT HABIT ---
class PleasantHabitViewSet(OwnerQuerysetMixin, ModelViewSet):
    serializer_class = PleasantHabitSerializer
    queryset = PleasantHabit.objects.all()
    pagination_class = ManualPagination

# --- USEFUL HABIT ---
class UsefulHabitViewSet(OwnerQuerysetMixin, ModelViewSet):
    serializer_class = UsefulHabitSerializer
    queryset = UsefulHabit.objects.all()
    pagination_class = ManualPagination

