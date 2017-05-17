# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import select_multiple_field.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('url', models.TextField()),
                ('width', models.PositiveIntegerField()),
                ('height', models.PositiveIntegerField()),
                ('direction', models.TextField()),
                ('img', models.ImageField(upload_to='../media/')),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='CUser',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('company', models.ForeignKey(to='counter.Company')),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('norm_name', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OptionsSet',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('camera', models.ForeignKey(to='counter.Camera')),
            ],
        ),
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('num', models.PositiveIntegerField()),
                ('direction', models.PositiveIntegerField()),
                ('datetime_start', models.DateTimeField()),
                ('datetime_end', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='TimeTable',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('date_s', models.DateField(default='01.01.2016', help_text='Дата начала')),
                ('time_s', models.TimeField(default='00:00', help_text='Время начала')),
                ('time_e', models.TimeField(default='01:00', help_text='Время конца')),
                ('days', select_multiple_field.models.SelectMultipleField(default='*', null=True, max_length=28, choices=[('Дни недели', (('0', 'Понедельник'), ('1', 'Вторник'), ('2', 'Среда'), ('3', 'Четверг'), ('4', 'Пятница'), ('5', 'Суббота'), ('6', 'Воскресенье')))], blank=True)),
                ('interval_length', models.IntegerField(default=300, choices=[(300, '5 минут'), (600, '10 минут'), (1800, '30 минут'), (3600, '1 час')], help_text='Время интервалов')),
                ('status', models.CharField(default='waiting', choices=[('done', 'завершено'), ('waiting', 'ожидает'), ('inprocess', 'в процессе'), ('deleted', 'удалено')], max_length=200)),
                ('camera', models.ForeignKey(to='counter.Camera')),
                ('group', models.ForeignKey(to='counter.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, help_text='Имя')),
                ('x1', models.PositiveIntegerField(help_text='x1')),
                ('y1', models.PositiveIntegerField(help_text='y1')),
                ('x2', models.PositiveIntegerField(help_text='x2')),
                ('y2', models.PositiveIntegerField(help_text='y2')),
                ('x3', models.PositiveIntegerField(help_text='x3')),
                ('y3', models.PositiveIntegerField(help_text='y3')),
                ('x4', models.PositiveIntegerField(help_text='x4')),
                ('y4', models.PositiveIntegerField(help_text='y4')),
                ('dir1', models.CharField(max_length=200, help_text='Вниз/влево')),
                ('dir2', models.CharField(max_length=200, help_text='Вверх/вправо')),
                ('camera', models.ForeignKey(help_text='Камера', to='counter.Camera')),
                ('directions', models.ForeignKey(help_text='Направление', to='counter.Direction')),
                ('group', models.ForeignKey(to='counter.Company')),
                ('user', models.ForeignKey(to='counter.CUser')),
            ],
        ),
        migrations.CreateModel(
            name='ZoneOption',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('min_object_area', models.PositiveIntegerField(default=10)),
                ('max_object_area', models.PositiveIntegerField(default=100)),
                ('rad', models.PositiveIntegerField(default=10)),
                ('set_rad', models.PositiveIntegerField(default=10)),
                ('blur', models.PositiveIntegerField(default=10)),
                ('sensitivity', models.PositiveIntegerField(default=30)),
                ('zone', models.ForeignKey(to='counter.Zone')),
            ],
        ),
        migrations.AddField(
            model_name='timetable',
            name='options',
            field=models.ManyToManyField(help_text='Набор настроек', to='counter.ZoneOption'),
        ),
        migrations.AddField(
            model_name='timetable',
            name='user',
            field=models.ForeignKey(to='counter.CUser'),
        ),
        migrations.AddField(
            model_name='results',
            name='zone_id',
            field=models.ForeignKey(to='counter.Zone'),
        ),
        migrations.AddField(
            model_name='optionsset',
            name='options',
            field=models.ManyToManyField(to='counter.ZoneOption'),
        ),
        migrations.AddField(
            model_name='camera',
            name='group',
            field=models.ManyToManyField(to='counter.Company'),
        ),
    ]
