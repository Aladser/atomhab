import os
from django.core.management import BaseCommand

from authen_drf.models import User
from libs.seeding import Seeding

user_1_email = os.getenv('MY_MAIL_1') if os.getenv('MY_MAIL_1') else 'user_1@test.ru'
user_2_email = os.getenv('MY_MAIL_2') if os.getenv('MY_MAIL_2') else 'user_2@test.ru'
user_3_email = os.getenv('MY_MAIL_3') if os.getenv('MY_MAIL_3') else 'user_3@test.ru'

user_obj_list = [
    {
        'email': user_1_email,
        'first_name': 'Админ',
        'last_name': 'Админов',
        'is_superuser': True,
        'is_staff': True
    },
    {
        'email': user_2_email,
        'first_name': 'Модератор',
        'last_name': 'Средний',
        'is_staff': True
    },
    {
        'email': user_3_email,
        'first_name': 'Пользователь',
        'last_name': 'Обычный',
        'is_staff': True
    }
]
password = '_strongpassword_'

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Seeding.seed_users(User, user_obj_list, password)
