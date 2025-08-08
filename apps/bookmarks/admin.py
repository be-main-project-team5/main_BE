from django.contrib import admin

from .models import GroupBookmark, IdolBookmark


@admin.register(IdolBookmark)
class IdolBookmarkAdmin(admin.ModelAdmin):
    list_display = ("user", "idol", "created_at")
    search_fields = ("user__email", "idol__name")
    raw_id_fields = ("user", "idol")  # 대량의 데이터에서 편리한 선택을 위해


@admin.register(GroupBookmark)
class GroupBookmarkAdmin(admin.ModelAdmin):
    list_display = ("user", "group", "created_at")
    search_fields = ("user__email", "group__name")
    raw_id_fields = ("user", "group")  # 대량의 데이터에서 편리한 선택을 위해
