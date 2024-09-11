import os

from django.core.management import BaseCommand
from django.contrib.auth.models import Group

from authen_drf.models import User
from libs.seeding import Seeding


class Command(BaseCommand):
    moderator_email = 'moderator@test.ru'
    user_mail = 'user@test.ru'

    user_obj_list = [
        {
            'email': 'admin@test.ru',
            'first_name': 'Админ',
            'last_name': 'Админов',
            'is_superuser': True,
            'is_staff': True
        },
        {
            'email': moderator_email,
            'first_name': 'Модератор',
            'last_name': 'Средний',
            'is_staff': True
        },
        {
            'email': user_mail,
            'first_name': 'Пользователь',
            'last_name': 'Обычный',
            'is_staff': True
        }
    ]

    password = '_strongpassword_'

    def handle(self, *args, **kwargs):
        if os.getenv('MY_MAIL_1'):
            self.user_obj_list[0]['email'] = os.getenv('MY_MAIL_1')
        if os.getenv('MY_MAIL_2'):
            self.user_obj_list[1]['email'] = os.getenv('MY_MAIL_2')
        if os.getenv('MY_MAIL_3'):
            self.user_obj_list[2]['email'] = os.getenv('MY_MAIL_3')

        Seeding.seed_users(User, self.user_obj_list, self.password)

        Group.objects.all().delete()
        moderators_group, created = Group.objects.get_or_create(name="moderators")

        if os.getenv('MY_MAIL_2'):
            moder = User.objects.get(email=os.getenv('MY_MAIL_2'))
        else:
            moder = User.objects.get(email=self.moderator_email)
        moder.groups.add(moderators_group)
        moder.save()

        if os.getenv('MY_MAIL_2'):
            user = User.objects.get(email=os.getenv('MY_MAIL_3'))
        else:
            user = User.objects.get(email=self.user_mail)
        users_group, created = Group.objects.get_or_create(name="users")
        user.groups.add(users_group)
        user.save()
