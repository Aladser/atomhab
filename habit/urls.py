from django.urls import path
from rest_framework.routers import DefaultRouter

from habit.apps import HabitConfig
from habit.views import LocationListAPIView, ActionListAPIView

app_name = HabitConfig.name

urlpatterns = [
    path('location/', LocationListAPIView.as_view(), name='location-list'),
    path('action/', ActionListAPIView.as_view(), name='action-list'),
    #path('reward/', RewardListAPIView.as_view(), name='reward-list'),
]
