from django.contrib import admin
from .models import Idol, IdolManager, IdolSchedule

admin.site.register(Idol)
admin.site.register(IdolManager)
admin.site.register(IdolSchedule)
