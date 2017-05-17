from django import forms
from .models import *
from select_multiple_field import forms as f


class ZoneForm(forms.ModelForm):
    class Meta:
        model = Zone
        exclude = (
            'camera',
            'user',
            'group',
        )


class TimeTableForm(forms.ModelForm):
    days = f.SelectMultipleFormField(required=False, choices=DAY_CHOICES)

    class Meta:
        model = TimeTable
        exclude = (
            'camera',
            'status',
            'user',
            'group',
            'interval_length'
        )


class ZoneOptionForm(forms.ModelForm):
    class Meta:
        model = ZoneOption
        exclude = (
            'zone',
        )
