from django.http import QueryDict
from rest_framework import serializers
from rest_framework.fields import empty

from habit.models import Location, Action, Reward, Habit, PleasantHabit, UsefulHabit, Periodicity
from libs.init_create_serializer_mixin import InitCreateSerializerMixin


class PeriodicitySerializer(serializers.ModelSerializer):
    """Периодичность"""

    class Meta:
        model = Periodicity
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    """Сериализатор местоположения"""

    class Meta:
        model = Location
        fields = '__all__'


class ActionSerializer(serializers.ModelSerializer):
    """Сериализатор действия"""

    class Meta:
        model = Action
        fields = '__all__'


class RewardSerializer(serializers.ModelSerializer):
    """Сериализатор вознаграждения"""

    class Meta:
        model = Reward
        fields = '__all__'


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор привычки"""

    class Meta:
        model = Habit
        fields = '__all__'


class HabitCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания привычки"""

    class Meta:
        model = Habit
        fields = '__all__'

    def __init__(self, instance=None, data=empty, **kwargs):
        if type(data) is not QueryDict:
            data['author'] = kwargs['context']['request'].user.pk
        super().__init__(instance, data, **kwargs)


class PleasantHabitSerializer(serializers.ModelSerializer):
    """Сериализатор приятной привычки"""

    class Meta:
        model = PleasantHabit
        fields = '__all__'


class PleasantHabitCreateSerializer(serializers.ModelSerializer, InitCreateSerializerMixin):
    """Сериализатор создания приятной привычки"""

    class Meta:
        model = PleasantHabit
        fields = '__all__'


class UsefulHabitSerializer(serializers.ModelSerializer):
    """Сериализатор полезной привычки"""

    class Meta:
        model = UsefulHabit
        fields = '__all__'


class UsefulCreateHabitSerializer(serializers.ModelSerializer, InitCreateSerializerMixin):
    """Сериализатор полезной привычки"""

    class Meta:
        model = UsefulHabit
        fields = '__all__'
