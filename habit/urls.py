from django.urls import path
from rest_framework.routers import DefaultRouter

from habit.apps import HabitConfig
from habit.views import LocationListAPIView, ActionListAPIView, RewardListAPIView, LocationCreateAPIView, \
    LocationDestroyAPIView, ActionCreateAPIView, ActionDestroyAPIView, RewardCreateAPIView, RewardDestroyAPIView, \
    HabitViewSet

app_name = HabitConfig.name

router = DefaultRouter()
router.register(r'habit', HabitViewSet, basename='habit')

urlpatterns = [
    path('location/', LocationListAPIView.as_view(), name='location-list'),
    path('location/create/', LocationCreateAPIView.as_view(), name='location-create'),
    path('location/<int:pk>/delete', LocationDestroyAPIView.as_view(), name='location-delete'),

    path('action/', ActionListAPIView.as_view(), name='action-list'),
    path('action/create/', ActionCreateAPIView.as_view(), name='action-create'),
    path('action/<int:pk>/delete', ActionDestroyAPIView.as_view(), name='action-delete'),

    path('reward/', RewardListAPIView.as_view(), name='reward-list'),
    path('reward/create/', RewardCreateAPIView.as_view(), name='reward-create'),
    path('reward/<int:pk>/delete', RewardDestroyAPIView.as_view(), name='reward-delete'),
]  + router.urls
