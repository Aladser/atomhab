from datetime import datetime

from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

from authen_drf.management.commands.createusers import user_1_email, user_2_email, user_3_email
from habit.models import *
from libs.seeding import Seeding

location_param_obj_list = [
    {'name': 'Дом'},
    {'name': 'Работа'},
    {'name': 'Двор'},
    {'name': 'Набережная'},
    {'name': 'Парк'},
    {'name': 'Озеро'},
]

action_param_obj_list = [
    {'name': 'петь', 'is_pleasant':True},
    {'name': 'играть', 'is_pleasant':True},
    {'name': 'танцевать', 'is_pleasant':True},
    {'name': 'бегать'},
    {'name': 'учиться'},
    {'name': 'отжиматься'},
]

reward_param_obj_list = [
    {'name': 'съесть банан'},
    {'name': 'полежать в кровати'},
    {'name': 'выпить воду'},
    {'name': 'играть с котом'},
    {'name': 'погулять на улице'},
]

periodicity_param_obj_list = [
    {'name':'1 час', 'interval': 60 * 60},
    {'name': '6 часов', 'interval': 60 * 60 * 6},
    {'name': '12 часов', 'interval': 60 * 60 * 12},
    {'name': '1 день', 'interval': 60 * 60 * 24},
    {'name': '3 дня', 'interval': 60 * 60 * 24 * 3},
    {'name': '1 неделя', 'interval': 60 * 60 * 24 * 7},
]

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Seeding.seed_table(Periodicity, periodicity_param_obj_list)
        Seeding.seed_table(Location, location_param_obj_list)
        Seeding.seed_table(Action, action_param_obj_list)
        Seeding.seed_table(Reward, reward_param_obj_list)

        place_1 =get_object_or_404(Location, name=location_param_obj_list[0]['name'])
        place_2 =get_object_or_404(Location, name=location_param_obj_list[1]['name'])
        place_3 =get_object_or_404(Location, name=location_param_obj_list[2]['name'])

        pleasant_action_1 =get_object_or_404(Action, name=action_param_obj_list[0]['name'])
        pleasant_action_2 =get_object_or_404(Action, name=action_param_obj_list[1]['name'])
        pleasant_action_3 =get_object_or_404(Action, name=action_param_obj_list[2]['name'])
        useful_action_1 =get_object_or_404(Action, name=action_param_obj_list[3]['name'])
        useful_action_2 =get_object_or_404(Action, name=action_param_obj_list[4]['name'])
        useful_action_3 =get_object_or_404(Action, name=action_param_obj_list[5]['name'])

        hour_period = get_object_or_404(Periodicity, name=periodicity_param_obj_list[0]['name'])
        day_period = get_object_or_404(Periodicity, name=periodicity_param_obj_list[3]['name'])
        week_period = get_object_or_404(Periodicity, name=periodicity_param_obj_list[5]['name'])

        userlist = [
            get_object_or_404(User, email=user_1_email),
            get_object_or_404(User, email=user_2_email),
            get_object_or_404(User, email=user_3_email)
        ]

        now_time = datetime.now().time()
        habit_param_obj_list = [
            {'location': place_1, 'action': pleasant_action_1, 'periodicity': hour_period, 'author':userlist[0], 'time':now_time, 'is_publiс':True},
            {'location': place_2, 'action': pleasant_action_2, 'periodicity': day_period, 'author':userlist[1], 'time':now_time},
            {'location': place_3, 'action': pleasant_action_3, 'periodicity': week_period, 'author':userlist[2], 'time':now_time},
            {'location':place_1, 'action': useful_action_1, 'periodicity': hour_period, 'author':userlist[0], 'time':now_time},
            {'location': place_2, 'action': useful_action_2, 'periodicity': day_period, 'author':userlist[1], 'time':now_time, 'is_publiс':True},
            {'location': place_3, 'action': useful_action_3, 'periodicity': week_period, 'author':userlist[2], 'time':now_time, 'is_publiс':True},
        ]
        Seeding.seed_table(Habit, habit_param_obj_list)

        pleasant_habits_param_obj_list = [
            {'habit': get_object_or_404(Habit, pk=1), 'user':userlist[0]},
            {'habit': get_object_or_404(Habit, pk=2), 'user':userlist[1]},
            {'habit': get_object_or_404(Habit, pk=3), 'user':userlist[2]}
        ]
        Seeding.seed_table(PleasantHabit, pleasant_habits_param_obj_list)
        reward =get_object_or_404(Reward, name=reward_param_obj_list[0]['name'])

        useful_habits_param_obj_list = [
            {'habit': get_object_or_404(Habit, pk=4), 'user':userlist[0]},
            {'habit': get_object_or_404(Habit, pk=5), 'user':userlist[1]},
            {'habit': get_object_or_404(Habit, pk=6), 'user':userlist[2]}
        ]
        Seeding.seed_table(UsefulHabit, useful_habits_param_obj_list)
