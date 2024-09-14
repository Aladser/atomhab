import datetime

def get_current_hour_time(offset:int = 0) -> datetime.time:
    """
    Возвращает time часа текущего времени
    :param offset: смещение относительно текущего времени
    """

    now_time = datetime.datetime.now().time()
    return datetime.time(hour=now_time.hour + offset, minute=0)


