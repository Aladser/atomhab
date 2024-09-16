from datetime import datetime

from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from authen_drf.management.commands.createusers import password, user_obj_list
from authen_drf.models import User
from habit.management.commands.seed import periodicity_param_obj_list, location_param_obj_list, action_param_obj_list, \
    reward_param_obj_list, seed_db_tables
from habit.models import Periodicity, Location, Action, Reward, Habit, PleasantHabit, UsefulHabit
from habit.tasks import check_habit_time
from libs.seeding import Seeding

"""
coverage run --source='.' manage.py test
coverage report или coverage html
"""
periodicity_params = {'name': 'test', 'interval': 61 * 60}
action_params = {'name': 'петь_', 'is_pleasant': True}
location_params = {'name': 'Дом 1'}


def get_test_authuser():
    """Возвращает тестового аутентифицированного пользователя """
    user_params = {'email': 'admin@test.ru', 'first_name': 'Админ', 'last_name': 'Админов', 'is_superuser': True}
    return User.objects.create(**user_params)


class PeriodicityTestCase(APITestCase):
    def setUp(self):
        self.client.force_authenticate(get_test_authuser())
        Seeding.seed_table(Periodicity, periodicity_param_obj_list)

    def test_list(self):
        url = reverse('habit:periodicity-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 6)

    def test_create(self):
        url = reverse('habit:periodicity-create')
        response = self.client.post(url, periodicity_params)
        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_json['name'], periodicity_params['name'])

        # Валидация периодичности - не больше 1 недели
        response = self.client.post(url, {'name': 'много', 'interval': 60 * 60 * 24 * 70})
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_json[0], 'Интервал периодичности не должен превышать одну неделю')

    def test_delete(self):
        url = reverse('habit:periodicity-delete', kwargs={'pk': 1})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Periodicity.objects.all().count(), 5)


class LocationTestCase(APITestCase):
    def setUp(self):
        self.client.force_authenticate(get_test_authuser())
        Seeding.seed_table(Location, location_param_obj_list)

    def test_list(self):
        url = reverse('habit:location-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), len(location_param_obj_list))


class ActionTestCase(APITestCase):
    def setUp(self):
        self.client.force_authenticate(user=get_test_authuser())
        Seeding.seed_table(Action, action_param_obj_list)

    def test_list(self):
        url = reverse('habit:action-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), len(action_param_obj_list))


class RewardTestCase(APITestCase):
    def setUp(self):
        self.client.force_authenticate(user=get_test_authuser())
        Seeding.seed_table(Reward, reward_param_obj_list)

    def test_list(self):
        url = reverse('habit:reward-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), len(reward_param_obj_list))


class HabitTestCase(APITestCase):
    def setUp(self):
        Seeding.seed_users(User, user_obj_list, password)
        self.client.force_authenticate(user=get_test_authuser())
        seed_db_tables()

        self.location = Location.objects.create(**location_params)
        self.action = Action.objects.create(**action_params)
        self.periodicity = Periodicity.objects.create(**periodicity_params)
        self.time = datetime.now().time()

    def test_list(self):
        url = reverse('habit:habit-list')
        response = self.client.get(url)

        place = Location.objects.get(id=1)
        action = Action.objects.get(id=1)
        hour = Periodicity.objects.get(id=1)
        user = User.objects.get(id=1)
        time = datetime.now().time()

        # Валидация времени исполнения
        habit_params = {'location': place, 'action': action, 'periodicity': hour, 'author': user, 'time': time,
                        'is_publiс': True, 'execution_time': 1000}
        with self.assertRaises(ValidationError):
            Habit.objects.create(**habit_params)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        url = '/habit/'
        habit_params = {
            "time": "20:04:00",
            "execution_time": 10,
            "location": 1,
            "action": 1,
            "periodicity": 2,
            'author': 1
        }
        response = self.client.post(url, habit_params)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(url, habit_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PleasantHabitTestCase(APITestCase):
    def setUp(self):
        Seeding.seed_users(User, user_obj_list, password)
        self.user = get_test_authuser()
        self.client.force_authenticate(user=self.user)
        seed_db_tables()

    def test_list(self):
        url = reverse('habit:pleasant-habit-list')
        response = self.client.get(url)

        pleasant_habit_params = {'habit': get_object_or_404(Habit, pk=4), 'user': self.user}
        # Валидация приятного действия
        with self.assertRaises(ValidationError):
            PleasantHabit.objects.create(**pleasant_habit_params)

        # Валидация разрешения пользователя использовать указанную привычку
        pleasant_habit_params = {'habit': get_object_or_404(Habit, pk=2), 'user': User.objects.get(id=3)}
        with self.assertRaises(ValidationError):
            PleasantHabit.objects.create(**pleasant_habit_params)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UsefulHabitTestCase(APITestCase):
    def setUp(self):
        Seeding.seed_users(User, user_obj_list, password)
        self.user = get_test_authuser()
        self.client.force_authenticate(user=self.user)
        seed_db_tables()

    def test_list(self):
        url = reverse('habit:useful-habit-list')
        response = self.client.get(url)

        # Нарушение валидации полезного действия
        useful_habit_params = {'habit': get_object_or_404(Habit, pk=1), 'user': self.user}
        with self.assertRaises(ValidationError):
            UsefulHabit.objects.create(**useful_habit_params)

        # Нарушение валидации указанного вознаграждения: полезная привычка или вознаграждение
        userful_habit = UsefulHabit()
        userful_habit.user = self.user
        userful_habit.habit = Habit.objects.get(pk=4)
        with self.assertRaises(ValidationError):
            userful_habit.save()

        # Нарушение валидации разрешения пользователя использовать неполезную привычку
        place = Location.objects.get(id=1)
        action = Action.objects.get(id=5)
        hour = Periodicity.objects.get(id=1)
        user = User.objects.get(id=1)
        time = datetime.now().time()
        habit_params = {'location': place, 'action': action, 'periodicity': hour, 'author': user, 'time': time,
                        'is_publiс': False, 'execution_time': 100}
        habit = Habit.objects.create(**habit_params)

        userful_habit = UsefulHabit()
        userful_habit.user = User.objects.get(pk=3)
        userful_habit.habit = habit
        userful_habit.reward = Reward.objects.get(pk=1)
        with self.assertRaises(ValidationError):
            userful_habit.save()

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DelayTaskTestCase(APITestCase):
    def setUp(self):
        self.client.force_authenticate(get_test_authuser())
        Seeding.seed_users(User, user_obj_list, password)
        seed_db_tables()

    def test_work(self):
        check_habit_time()
