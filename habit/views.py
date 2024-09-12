from rest_framework import generics

from habit.models import Location
from habit.serializers import LocationSerializer


# LOCATION LIST
class LocationListAPIView(generics.ListAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()

