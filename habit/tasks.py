from celery import shared_task


@shared_task
def check_habit_time():
    return 'test'
