import datetime
import os, requests

from celery import shared_task


from habit.models import UsefulHabit, Habit, PleasantHabit
from libs.get_current_hour_time import get_current_hour_time

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

@shared_task
def check_habit_time():
    """
        Рассылка уведомлений о выполнении привычек, которые будут в ближайший час
    """

    now_datetime = datetime.datetime.now()
    now_time_start = get_current_hour_time()
    now_time_end = get_current_hour_time(1)

    nearest_habits_list = list(Habit.objects.filter(time__gt=now_time_start, time__lt=now_time_end))
    useful_habits_list = UsefulHabit.objects.filter(habit__in=nearest_habits_list)
    pleasant_habits_list = PleasantHabit.objects.filter(habit__in=nearest_habits_list)

    sending_list = []
    chat_list = []
    fill_sending_list(useful_habits_list, sending_list, chat_list, "Полезная привычка")
    fill_sending_list(pleasant_habits_list, sending_list, chat_list, "Приятная привычка")

    if len(sending_list) > 0:
        [send_message.delay(chat, f"{str(now_datetime)[:16]} Напоминаю о ближайших привычках:") for chat in chat_list]
        [send_message.delay(sending["chat_id"], sending["text"]) for sending in sending_list]
    return '\n' + '\n'.join([sending["text"] for sending in sending_list])


@shared_task
def send_message(chat_id, text):
    """Отправляет отложенно сообщение в телеграм """

    params = {
        "text": text,
        "chat_id": chat_id
    }
    response = requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", params=params)

    print(response.__dict__['url'])
    print(response.__dict__['_content'])

def fill_sending_list(habits_list, sending_list, chat_list, text):
    """Заполняет список рассылок уведомлений"""

    for habit in habits_list:
        obj = {
            "text": text + ": " + str(habit.habit),
            "chat_id": habit.user.tg_chat_id
        }
        sending_list.append(obj)
        if habit.user.tg_chat_id not in chat_list:
            chat_list.append(habit.user.tg_chat_id)
