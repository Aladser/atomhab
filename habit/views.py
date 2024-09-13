from rest_framework import generics

from habit.models import Location, Action, Reward
from habit.serializers import LocationSerializer, ActionSerializer, RewardSerializer


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
