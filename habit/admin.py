from django.contrib import admin

from habit.models import Periodicity, Location, Action, Reward, Habit, PleasantHabit, UsefulHabit


@admin.register(Periodicity)
class DatePeriodAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'interval')
    search_fields = ('name',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)
    search_fields = ('name',)

@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)
    search_fields = ('name',)

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'is_pleasant')
    search_fields = ('name',)

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'location', 'action', 'time', 'periodicity', 'execution_time', 'is_publiс')

@admin.register(PleasantHabit)
class PleasantHabit(admin.ModelAdmin):
    list_display = ('pk', 'user', 'habit')

@admin.register(UsefulHabit)
class UsefulHabit(admin.ModelAdmin):
    list_display = ('pk', 'user', 'habit', 'pleasant_habit', 'reward')
