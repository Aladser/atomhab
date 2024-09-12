from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

from authen_drf.management.commands.createusers import user_1_email, user_2_email, user_3_email
from habit.models import *
from libs.seeding import Seeding

place_param_obj_list = [
    {'name': 'Дом'},
    {'name': 'Работа'},
    {'name': 'Двор'},
    {'name': 'Набережная'},
    {'name': 'Парк'},
]

action_param_obj_list = [
    {'name': 'бегать'},
    {'name': 'учиться'},
    {'name': 'отжиматься'},
    {'name': 'петь'},
    {'name': 'играть'},
    {'name': 'танцевать'},
    {'name': 'убираться'},
    {'name': 'кормить кота'},
    {'name': 'убираться'},
]

reward_param_obj_list = [
    {'name': 'съесть банан'},
    {'name': 'полежать в кровати'},
    {'name': 'выпить воду'},
    {'name': 'играть с котом'},
    {'name': 'погулять на улице'},
]

dateperiod_param_obj_list = [
    {'name':'1 час', 'interval': 60 * 60},
    {'name': '6 часов', 'interval': 60 * 60 * 6},
    {'name': '12 часов', 'interval': 60 * 60 * 12},
    {'name': '1 день', 'interval': 60 * 60 * 24},
    {'name': '3 дня', 'interval': 60 * 60 * 24 * 3},
    {'name': '1 неделя', 'interval': 60 * 60 * 24 * 7},
]

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Seeding.seed_table(DatePeriod, dateperiod_param_obj_list)
        Seeding.seed_table(Place, place_param_obj_list)
        Seeding.seed_table(Action, action_param_obj_list)
        Seeding.seed_table(Reward, reward_param_obj_list)

        user_1 = get_object_or_404(User, email=user_1_email)
        user_2 = get_object_or_404(User, email=user_2_email)
        user_3 = get_object_or_404(User, email=user_3_email)

        place_1 =get_object_or_404(Place, name=place_param_obj_list[0]['name'])
        place_2 =get_object_or_404(Place, name=place_param_obj_list[1]['name'])
        place_3 =get_object_or_404(Place, name=place_param_obj_list[2]['name'])

        action_1 =get_object_or_404(Action, name=action_param_obj_list[0]['name'])
        action_2 =get_object_or_404(Action, name=action_param_obj_list[1]['name'])
        action_3 =get_object_or_404(Action, name=action_param_obj_list[2]['name'])

        reward_1 =get_object_or_404(Reward, name=reward_param_obj_list[0]['name'])
        reward_2 =get_object_or_404(Reward, name=reward_param_obj_list[1]['name'])
        reward_3 =get_object_or_404(Reward, name=reward_param_obj_list[2]['name'])

        hour_period = get_object_or_404(DatePeriod, name=dateperiod_param_obj_list[0]['name'])
        day_period = get_object_or_404(DatePeriod, name=dateperiod_param_obj_list[3]['name'])
        week_period = get_object_or_404(DatePeriod, name=dateperiod_param_obj_list[5]['name'])

        habit_param_obj_list = [
            {'location':place_1, 'action':action_1, 'periodicity': hour_period},
            {'location': place_2, 'action': action_2, 'periodicity': day_period},
            {'location': place_3, 'action': action_3, 'periodicity': week_period},
        ]
        Seeding.seed_table(Habit, habit_param_obj_list)


