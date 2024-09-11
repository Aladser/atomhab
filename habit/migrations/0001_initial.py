# Generated by Django 5.1.1 on 2024-09-11 13:50

import django.db.models.deletion
import libs.truncate_table_mixin
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Объяснение')),
            ],
            options={
                'verbose_name': 'Действие',
                'verbose_name_plural': 'Действия',
                'ordering': ('name',),
            },
            bases=(libs.truncate_table_mixin.TruncateTableMixin, models.Model),
        ),
        migrations.CreateModel(
            name='DatePeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Название')),
                ('interval', models.PositiveIntegerField(verbose_name='Интервал (в секундах)')),
            ],
            options={
                'verbose_name': 'Интервал рассылки',
                'verbose_name_plural': 'интервалы рассылки',
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Комментарии')),
            ],
            options={
                'verbose_name': 'Место',
                'verbose_name_plural': 'Места',
                'ordering': ('pk',),
            },
            bases=(libs.truncate_table_mixin.TruncateTableMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Объяснение')),
            ],
            options={
                'verbose_name': 'Вознаграждение',
                'verbose_name_plural': 'Вознаграждения',
                'ordering': ('name',),
            },
            bases=(libs.truncate_table_mixin.TruncateTableMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now=True, verbose_name='Время')),
                ('is_pleasant', models.BooleanField(default=False, verbose_name='Признак приятной привычки')),
                ('execution_time', models.PositiveIntegerField(default=120, verbose_name='Время выполнения, в секундах')),
                ('is_published', models.BooleanField(default=False, verbose_name='Признак публикации')),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='habits', to='habit.action', verbose_name='Действие')),
                ('interval', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='habits', to='habit.dateperiod', verbose_name='Периодичность')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='habits', to=settings.AUTH_USER_MODEL, verbose_name='Создатель')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='habits', to='habit.place', verbose_name='Место')),
                ('reward', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='habits', to='habit.reward', verbose_name='Вознаграждение')),
            ],
            options={
                'verbose_name': 'Привычка',
                'verbose_name_plural': 'Привычки',
                'ordering': ('-pk',),
            },
            bases=(libs.truncate_table_mixin.TruncateTableMixin, models.Model),
        ),
        migrations.CreateModel(
            name='RelatedHabit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('related_link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_habits', to='habit.habit', verbose_name='привычка')),
            ],
            options={
                'verbose_name': 'Связанная привычка',
                'verbose_name_plural': 'Связанные привычки',
                'ordering': ('-pk',),
            },
            bases=(libs.truncate_table_mixin.TruncateTableMixin, models.Model),
        ),
    ]
