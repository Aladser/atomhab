from rest_framework import generics

from habit.models import Location, Action, Reward
from habit.serializers import LocationSerializer, ActionSerializer, RewardSerializer


# LOCATION LIST
class LocationListAPIView(generics.ListAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()

# ACTION LIST
class ActionListAPIView(generics.ListAPIView):
    serializer_class = ActionSerializer
    queryset = Action.objects.all()

# REWARD LIST
class RewardListAPIView(generics.ListAPIView):
    serializer_class = RewardSerializer
    queryset = Reward.objects.all()
