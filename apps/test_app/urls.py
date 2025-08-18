from django.urls import path
from . import views

urlpatterns = [
    # 인증
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),

    # 역할별 메인 페이지
    path("fan/", views.fan_favorites_view, name="fan_favorites"),
    path("idol/", views.idol_mainboard_view, name="idol_mainboard"),
    path("manager/", views.manager_mainboard_view, name="manager_mainboard"),
    path("admin/", views.admin_mainboard_view, name="test_admin_main"),

    # 데이터 목록
    path("idols/", views.idol_list_view, name="idol_list"),
    path("groups/", views.group_list_view, name="group_list"),
    path("my_schedules/", views.my_schedules_view, name="my_schedules"),

    # 데이터 상세 정보
    path("idols/<int:idol_id>/", views.idol_detail_view, name="idol_detail"),

    # 기능 (Action)
    path("bookmark_idol/<int:idol_id>/", views.bookmark_idol_view, name="bookmark_idol"),
    path("bookmark_group/<int:group_id>/", views.bookmark_group_view, name="bookmark_group"),
    path("add_user_schedule/<int:schedule_id>/", views.add_user_schedule_view, name="add_user_schedule"),
    path("add_schedule/", views.add_schedule_view, name="add_schedule"),

    # 관리자/매니저 기능
    path("create_group/", views.create_group_view, name="create_group"),
    path("update_idol_group/<int:idol_id>/", views.update_idol_group_view, name="update_idol_group"),
    path("admin/create_manager/", views.admin_create_manager_view, name="test_admin_create_manager"),
    path("admin/create_idol/", views.admin_create_idol_view, name="test_admin_create_idol"),
    path("admin/delete_user/<int:user_id>/", views.admin_delete_user_view, name="test_admin_delete_user"),
    path("admin/assign_manager/", views.admin_assign_manager_view, name="test_admin_assign_manager"),
    path("admin/unassign_manager/<int:assignment_id>/", views.admin_unassign_manager_view, name="test_admin_unassign_manager"),
    path("admin/update_idol_group/<int:idol_id>/", views.admin_update_idol_group_view, name="test_admin_update_idol_group"),

    # 분리된 테스트 뷰
    path("manager_schedule_test/", views.manager_schedule_test_view, name="manager_schedule_test"),
]
