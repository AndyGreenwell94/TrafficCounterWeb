import django_tables2 as tables
from .models import *


class ResultTable(tables.Table):
    class Meta:
        model = Results
        attrs = {}