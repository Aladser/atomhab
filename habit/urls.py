from django.urls import path
from rest_framework.routers import DefaultRouter

from habit.apps import HabitConfig
from habit.views import HabitViewSet, UsefulHabitViewSet, PleasantHabitViewSet, PeriodicityListAPIView, \
    PeriodicityCreateAPIView, PeriodicityDestroyAPIView, LocationListAPIView, LocationCreateAPIView, \
    LocationDestroyAPIView, ActionListAPIView, ActionCreateAPIView, ActionDestroyAPIView, RewardListAPIView, \
    RewardCreateAPIView, RewardDestroyAPIView, PublicHabitListAPIView

app_name = HabitConfig.name

router = DefaultRouter()
router.register(r'habit', HabitViewSet, 'habit')
router.register(r'pleasant-habit', PleasantHabitViewSet, 'pleasant-habit')
router.register(r'useful-habit', UsefulHabitViewSet, 'useful-habit')

urlpatterns = [
    path('periodicity/', PeriodicityListAPIView.as_view(), name='periodicity-list'),
    path('periodicity/create/', PeriodicityCreateAPIView.as_view(), name='periodicity-create'),
    path('periodicity/<int:pk>/delete', PeriodicityDestroyAPIView.as_view(), name='periodicity-delete'),

    path('location/', LocationListAPIView.as_view(), name='location-list'),
    path('location/create/', LocationCreateAPIView.as_view(), name='location-create'),
    path('location/<int:pk>/delete', LocationDestroyAPIView.as_view(), name='location-delete'),

    path('action/', ActionListAPIView.as_view(), name='action-list'),
    path('action/create/', ActionCreateAPIView.as_view(), name='action-create'),
    path('action/<int:pk>/delete', ActionDestroyAPIView.as_view(), name='action-delete'),

    path('reward/', RewardListAPIView.as_view(), name='reward-list'),
    path('reward/create/', RewardCreateAPIView.as_view(), name='reward-create'),
    path('reward/<int:pk>/delete', RewardDestroyAPIView.as_view(), name='reward-delete'),

    path('public-habit/', PublicHabitListAPIView.as_view(), name='public-habit'),
] + router.urls
