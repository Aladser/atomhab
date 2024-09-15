from rest_framework import serializers

from habit.models import Location, Action, Reward, Habit, PleasantHabit, UsefulHabit, Periodicity


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


class PleasantHabitSerializer(serializers.ModelSerializer):
    """Сериализатор приятной привычки"""

    class Meta:
        model = PleasantHabit
        fields = '__all__'


class UsefulHabitSerializer(serializers.ModelSerializer):
    """Сериализатор полезной привычки"""

    class Meta:
        model = UsefulHabit
        fields = '__all__'
