from django.contrib import admin

from .models import Idol, IdolManager

class IdolAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'display_manager')
    list_filter = ('group',)

    def display_manager(self, obj):
        managers = IdolManager.objects.filter(idol=obj)
        if managers.exists():
            return ", ".join([manager.user.nickname for manager in managers])
        return "(None)"
    display_manager.short_description = 'Manager'

admin.site.register(Idol, IdolAdmin)
admin.site.register(IdolManager)