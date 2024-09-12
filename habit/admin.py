from django.contrib import admin

from habit.models import DatePeriod, Location, Action, Reward, Habit


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
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('location', 'action', 'time', 'periodicity', 'execution_time', 'is_publiс')


