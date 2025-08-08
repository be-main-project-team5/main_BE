from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.bookmarks.models import IdolBookmark, GroupBookmark
from apps.schedules.models import UserSchedule, IdolSchedule, GroupSchedule

@receiver(post_save, sender=IdolBookmark)
def add_idol_schedules_to_user_schedule(sender, instance, created, **kwargs):
    if created: # 새로운 IdolBookmark가 생성되었을 때만 실행
        user = instance.user
        idol = instance.idol
        # 해당 아이돌의 모든 스케줄을 가져옴
        idol_schedules = IdolSchedule.objects.filter(idol=idol)
        for idol_schedule in idol_schedules:
            # UserSchedule에 추가 (이미 존재하면 생성하지 않음)
            UserSchedule.objects.get_or_create(user=user, idol_schedule=idol_schedule)

@receiver(post_save, sender=GroupBookmark)
def add_group_schedules_to_user_schedule(sender, instance, created, **kwargs):
    if created: # 새로운 GroupBookmark가 생성되었을 때만 실행
        user = instance.user
        group = instance.group
        # 해당 그룹의 모든 스케줄을 가져옴
        group_schedules = GroupSchedule.objects.filter(group=group)
        for group_schedule in group_schedules:
            # UserSchedule에 추가 (이미 존재하면 생성하지 않음)
            UserSchedule.objects.get_or_create(user=user, group_schedule=group_schedule)

@receiver(post_delete, sender=IdolBookmark)
def remove_idol_schedules_from_user_schedule(sender, instance, **kwargs):
    user = instance.user
    idol = instance.idol
    # 해당 아이돌의 모든 스케줄을 가져와 UserSchedule에서 제거
    UserSchedule.objects.filter(user=user, idol_schedule__idol=idol).delete()

@receiver(post_delete, sender=GroupBookmark)
def remove_group_schedules_from_user_schedule(sender, instance, **kwargs):
    user = instance.user
    group = instance.group
    # 해당 그룹의 모든 스케줄을 가져와 UserSchedule에서 제거
    UserSchedule.objects.filter(user=user, group_schedule__group=group).delete()
