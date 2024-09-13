import datetime

from django.db import IntegrityError
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet

from habit.models import Location, Action, Reward, Habit
from habit.serializers import LocationSerializer, ActionSerializer, RewardSerializer, HabitSerializer


# LOCATION LIST
class LocationListAPIView(generics.ListAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()

# LOCATION CREATE
class LocationCreateAPIView(generics.CreateAPIView):
    serializer_class = LocationSerializer

# LOCATION DESTROY
class LocationDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()


# ACTION LIST
class ActionListAPIView(generics.ListAPIView):
    serializer_class = ActionSerializer
    queryset = Action.objects.all()

# ACTION CREATE
class ActionCreateAPIView(generics.CreateAPIView):
    serializer_class = ActionSerializer

# ACTION DESTROY
class ActionDestroyAPIView(generics.DestroyAPIView):
    serializer_class = ActionSerializer
    queryset = Action.objects.all()


# REWARD LIST
class RewardListAPIView(generics.ListAPIView):
    serializer_class = RewardSerializer
    queryset = Reward.objects.all()

# REWARD CREATE
class RewardCreateAPIView(generics.CreateAPIView):
    serializer_class = RewardSerializer

# REWARD DESTROY
class RewardDestroyAPIView(generics.DestroyAPIView):
    serializer_class = RewardSerializer
    queryset = Reward.objects.all()

# --- HABIT ---
class HabitViewSet(ModelViewSet):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()

    def perform_create(self, serializer):
        habit = serializer.save()
        # округляет время
        habit.time = datetime.time(habit.time.hour, habit.time.minute)
        try:
            habit.save()
        except IntegrityError as e:
            raise ValidationError(f"<<{str(habit)}>>: дубликат привычки")



