from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from authen_drf.models import User
from habit.management.commands.seed import periodicity_param_obj_list
from habit.models import Periodicity
from libs.seeding import Seeding

"""
coverage run --source='.' manage.py test
coverage report
"""
user_params = {'email': 'admin@test.ru','first_name': 'Админ','last_name': 'Админов', 'is_superuser': True}
periodicity_params = {'pk':1, 'name':'11 час', 'interval': 61 * 60}

class PeriodicityTestCase(APITestCase):
    def setUp(self):
        User.objects.create(**user_params)
        self.user = User.objects.get(email=user_params['email'])
        self.client.force_authenticate(user=self.user)
        Seeding.seed_table(Periodicity, periodicity_param_obj_list)

    def test_list(self):
        url = reverse('habit:periodicity-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 6)

    def test_create(self):
        url = reverse('habit:periodicity-create')
        response = self.client.post(url, periodicity_params)
        received_lesson = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(received_lesson['name'], periodicity_params['name'])

    def test_delete(self):
        url = reverse('habit:periodicity-delete', kwargs={'pk': 1})
        response  = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Periodicity.objects.all().count(), 5)
