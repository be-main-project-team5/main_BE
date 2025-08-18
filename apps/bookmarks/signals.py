from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.bookmarks.models import GroupBookmark, IdolBookmark
from apps.idols.models import Idol
from apps.schedules.models import GroupSchedule, IdolSchedule, UserSchedule


@receiver(post_save, sender=IdolBookmark)
def add_idol_schedules_to_user_schedule(sender, instance, created, **kwargs):
    """아이돌 북마크 시, 해당 아이돌의 모든 스케줄을 사용자 스케줄에 추가"""
    if created:
        user = instance.user
        idol = instance.idol
        idol_schedules = IdolSchedule.objects.filter(idol=idol)
        for idol_schedule in idol_schedules:
            UserSchedule.objects.get_or_create(user=user, idol_schedule=idol_schedule)


@receiver(post_delete, sender=IdolBookmark)
def remove_idol_schedules_from_user_schedule(sender, instance, **kwargs):
    """아이돌 북마크 해제 시, 해당 아이돌의 스케줄을 사용자 스케줄에서 제거"""
    user = instance.user
    idol = instance.idol
    UserSchedule.objects.filter(user=user, idol_schedule__idol=idol).delete()


@receiver(post_save, sender=GroupBookmark)
def add_group_schedules_to_user_schedule(sender, instance, created, **kwargs):
    """그룹 북마크 시, 해당 그룹에 속한 모든 아이돌의 스케줄을 사용자 스케줄에 추가"""
    if created:
        user = instance.user
        group = instance.group
        # 그룹에 속한 모든 아이돌을 가져옴
        idols_in_group = Idol.objects.filter(group=group)
        # 해당 아이돌들의 모든 스케줄을 가져옴
        idol_schedules = IdolSchedule.objects.filter(idol__in=idols_in_group)
        for idol_schedule in idol_schedules:
            UserSchedule.objects.get_or_create(user=user, idol_schedule=idol_schedule)
        # 그룹 자체의 스케줄도 추가
        group_schedules = GroupSchedule.objects.filter(group=group)
        for group_schedule in group_schedules:
            UserSchedule.objects.get_or_create(user=user, group_schedule=group_schedule)


@receiver(post_delete, sender=GroupBookmark)
def remove_group_schedules_from_user_schedule(sender, instance, **kwargs):
    """그룹 북마크 해제 시, 해당 그룹 및 소속 아이돌의 스케줄을 사용자 스케줄에서 제거"""
    user = instance.user
    group = instance.group
    # 그룹에 속한 모든 아이돌을 가져옴
    idols_in_group = Idol.objects.filter(group=group)
    # 해당 아이돌들의 스케줄을 UserSchedule에서 제거
    UserSchedule.objects.filter(
        user=user, idol_schedule__idol__in=idols_in_group
    ).delete()
    # 그룹 자체의 스케줄도 제거
    UserSchedule.objects.filter(user=user, group_schedule__group=group).delete()
