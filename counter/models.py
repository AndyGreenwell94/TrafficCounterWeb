from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from select_multiple_field import models as m
import datetime

DAY_CHOICES = (('Дни недели', (('0', 'Понедельник'),
                               ('1', 'Вторник'),
                               ('2', 'Среда'),
                               ('3', 'Четверг'),
                               ('4', 'Пятница'),
                               ('5', 'Суббота'),
                               ('6', 'Воскресенье'),
                               )),)

class Company(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class CUser(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Camera(models.Model):
    group = models.ManyToManyField(Company)
    name = models.CharField(max_length=200)
    url = models.TextField()
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    direction = models.TextField()
    img = models.ImageField(upload_to='../media/')

    def active_tt(self):
        if self.timetable_set.filter(status='active'):
            self.timetable_set.filter(status='active').count()
            return self.timetable_set.filter(status='active').count()

    def active_now(self):
        a = False
        for t in self.timetable_set.all().filter(status='active'):
            if datetime.datetime.now().time() > t.time_s and datetime.datetime.now().time() < t.time_e:
                a = True
        return a


    def __str__(self):
        return self.name+'   '+self.url


class Direction(models.Model):
    name = models.CharField(max_length=200)
    norm_name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.norm_name


class Zone(models.Model):
    user = models.ForeignKey(CUser)
    group = models.ForeignKey(Company)
    name = models.CharField(max_length=200, help_text='Имя')
    x1 = models.PositiveIntegerField(help_text='x1', )
    y1 = models.PositiveIntegerField(help_text='y1')
    x2 = models.PositiveIntegerField(help_text='x2')
    y2 = models.PositiveIntegerField(help_text='y2')
    x3 = models.PositiveIntegerField(help_text='x3')
    y3 = models.PositiveIntegerField(help_text='y3')
    x4 = models.PositiveIntegerField(help_text='x4')
    y4 = models.PositiveIntegerField(help_text='y4')
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, help_text='Камера')
    dir1 = models.CharField(max_length=200, help_text='Вниз/влево')
    dir2 = models.CharField(max_length=200, help_text='Вверх/вправо')
    directions = models.ForeignKey(Direction, on_delete=models.CASCADE, help_text='Направление')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('zone-detail', kwargs={'pk': self.pk})


class ZoneOption(models.Model):
    name = models.CharField(max_length=200)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    min_object_area = models.PositiveIntegerField(default=10)
    max_object_area = models.PositiveIntegerField(default=100)
    rad = models.PositiveIntegerField(default=10)
    set_rad = models.PositiveIntegerField(default=10)
    blur = models.PositiveIntegerField(default=10)
    sensitivity = models.PositiveIntegerField(default=30)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('zoneop-detail', kwargs={'pk': self.pk})


class OptionsSet(models.Model):
    name = models.CharField(max_length=200)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    options = models.ManyToManyField(ZoneOption)

    def __str__(self):
        return self.name


class TimeTable(models.Model):
    user = models.ForeignKey(CUser)
    group = models.ForeignKey(Company)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    date_s = models.DateField(help_text='Дата начала', default='01.01.2016')
    time_s = models.TimeField(help_text='Время начала', default='00:00')
    time_e = models.TimeField(help_text='Время конца', default='01:00')
    days = m.SelectMultipleField(choices=DAY_CHOICES, max_length=28, blank=True, default='*', null=True)
    INTERVAL_CHOISES = ((300, "5 минут"),
                        (600, "10 минут"),
                        (1800, "30 минут"),
                        (3600, "1 час"),)
    interval_length = models.IntegerField(help_text='Время интервалов', choices=INTERVAL_CHOISES, default=300)
    status = models.CharField(choices=(('done', 'завершено'),
                                       ('waiting', 'ожидает'),
                                       ('inprocess', 'в процессе'),
                                       ('deleted', 'удалено')), max_length=200, default='waiting')
    options = models.ManyToManyField(ZoneOption, help_text='Набор настроек')

    def __str__(self):
        return str(self.date_s)+' '+str(self.time_s)


class Results(models.Model):
    num = models.PositiveIntegerField()
    direction = models.PositiveIntegerField()
    datetime_start = models.DateTimeField()
    datetime_end = models.DateTimeField()
    zone_id = models.ForeignKey(Zone, on_delete=models.CASCADE)