from django.contrib import admin

from habit.models import DatePeriod, Place, Action, Reward, Habit, RelatedHabit


@admin.register(DatePeriod)
class DatePeriodAdmin(admin.ModelAdmin):
    list_display = ('name', 'interval')
    search_fields = ('name',)

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('address', 'description')
    search_fields = ('address',)

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('user', 'place', 'datetime', 'action', 'is_pleasant', 'interval', 'reward', 'execution_time', 'is_published')
    search_fields = ('name',)

@admin.register(RelatedHabit)
class RelatedHabitAdmin(admin.ModelAdmin):
    list_display = ('pk', 'related_link')
    search_fields = ('pk',)
