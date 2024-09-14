import datetime

from celery import shared_task

from habit.models import UsefulHabit, Habit, PleasantHabit


@shared_task
def check_habit_time():
    """
        Рассылка уведомлений о выполнении привычек, которые будут в ближайший час
    """

    now_datetime = datetime.datetime.now().time()
    now_time_start = datetime.time(hour=now_datetime.hour, minute=0)
    now_time_end = datetime.time(hour=now_datetime.hour+1, minute=0)

    nearest_habits_list = list(Habit.objects.filter(time__gt=now_time_start, time__lt=now_time_end))
    useful_habits_list = UsefulHabit.objects.filter(habit__in=nearest_habits_list)
    pleasant_habits_list = PleasantHabit.objects.filter(habit__in=nearest_habits_list)
    nearest_active_habits_list = list(useful_habits_list)

    [nearest_active_habits_list.append(habit) for habit in pleasant_habits_list]
    return '\n'+'\n'.join([str(habit) for habit in nearest_active_habits_list])


