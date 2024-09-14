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

    sending_list = []
    for habit in useful_habits_list:
        row = f"ID телеграм чата {habit.user.tg_chat_id}: {habit.habit.action} в {habit.habit.time} в {habit.habit.location}"
        sending_list.append(row)
    for habit in pleasant_habits_list:
        row = f"ID телеграм чата {habit.user.tg_chat_id}: {habit.habit.action} в {habit.habit.time} в {habit.habit.location}"
        sending_list.append(row)
    return '\n'+'\n'.join(sending_list)


