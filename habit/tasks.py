import datetime
import os, requests

from celery import shared_task


from habit.models import UsefulHabit, Habit, PleasantHabit
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

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
        obj = {
            "row": f"ID телеграм чата {habit.user.tg_chat_id}: {habit.habit.action} в {habit.habit.time} в {habit.habit.location}",
            "habit": str(habit),
            "chat_id": habit.user.tg_chat_id
        }
        sending_list.append(obj)
    for habit in pleasant_habits_list:
        obj = {
            "row": f"ID телеграм чата {habit.user.tg_chat_id}: {habit.habit.action} в {habit.habit.time} в {habit.habit.location}",
            "habit": habit,
            "chat_id": habit.user.tg_chat_id
        }
        sending_list.append(obj)

    if len(sending_list) > 0:
            [send_message.delay(sending["chat_id"], str(sending["habit"])) for sending in sending_list]
    return '\n' + '\n'.join([sending["row"] for sending in sending_list])


@shared_task
def send_message(chat_id, text):
    """Отправляет отложенно сообщение в телеграм """

    params = {
        "chat_id": chat_id,
        "text": text
    }
    response = requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", params=params)

    print(response.__dict__['url'])
    print(response.__dict__['_content'])
