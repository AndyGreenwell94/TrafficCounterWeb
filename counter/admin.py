from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Camera)
admin.site.register(Zone)
admin.site.register(ZoneOption)
admin.site.register(Direction)
admin.site.register(OptionsSet)
admin.site.register(TimeTable)
admin.site.register(CUser)
admin.site.register(Company)
admin.site.register(Results)