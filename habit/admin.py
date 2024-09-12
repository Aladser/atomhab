from django.contrib import admin

from habit.models import DatePeriod, Location, Action, Reward, Habit, PleasantHabit, UsefulHabit, UserUsefulHabit


@admin.register(DatePeriod)
class DatePeriodAdmin(admin.ModelAdmin):
    list_display = ('name', 'interval')
    search_fields = ('name',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_pleasant')
    search_fields = ('name',)

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'location', 'action', 'time', 'periodicity', 'execution_time', 'is_publiс')

@admin.register(PleasantHabit)
class PleasantHabit(admin.ModelAdmin):
    list_display = ('pk', 'habit')

@admin.register(UsefulHabit)
class UsefulHabit(admin.ModelAdmin):
    list_display = ('pk', 'habit', 'pleasant_habit', 'reward')

@admin.register(UserUsefulHabit)
class UserUsefulHabit(admin.ModelAdmin):
    list_display = ('pk', 'user', 'useful_habit')
