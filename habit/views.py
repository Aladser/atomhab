import datetime
from lib2to3.fixes.fix_input import context

from django.core.exceptions import ValidationError
from rest_framework import generics, exceptions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from authen_drf.permissions import IsAuthorPermission
from habit.models import Location, Action, Reward, Habit, PleasantHabit, UsefulHabit, Periodicity
from habit.paginators import ManualPagination
from habit.serializers import LocationSerializer, ActionSerializer, RewardSerializer, HabitSerializer, \
    PleasantHabitSerializer, UsefulHabitSerializer, PeriodicitySerializer
from libs.queryset_mixin import AuthorQuerysetMixin


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
class HabitViewSet(AuthorQuerysetMixin, ModelViewSet):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = ManualPagination

    def get_permissions(self):
        if self.action in ['detail', 'update', 'partial_update', 'delete']:
            self.permission_classes = [IsAuthorPermission]
        return super().get_permissions()

    def get_serializer(self, *args, **kwargs):
        if self.action == 'create':
            kwargs['data']['author'] = self.request.user.pk
        return super().get_serializer(*args, **kwargs)

    def perform_create(self, serializer):
        habit = serializer.save()
        # округляет время
        habit.time = datetime.time(habit.time.hour, habit.time.minute)
        try:
            habit.save()
        except ValidationError as e:
            raise exceptions.ValidationError(f"Привычка <<{habit}>> уже существует")

# --- PLEASANT HABIT ---
class PleasantHabitViewSet(AuthorQuerysetMixin, ModelViewSet):
    serializer_class = PleasantHabitSerializer
    queryset = PleasantHabit.objects.all()
    pagination_class = ManualPagination

# --- USEFUL HABIT ---
class UsefulHabitViewSet(AuthorQuerysetMixin, ModelViewSet):
    serializer_class = UsefulHabitSerializer
    queryset = UsefulHabit.objects.all()
    pagination_class = ManualPagination



