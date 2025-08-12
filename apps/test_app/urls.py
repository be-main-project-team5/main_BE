from django.urls import path

from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("idols/", views.idol_list_view, name="idol_list"),
    path("groups/", views.group_list_view, name="group_list"),
    path(
        "bookmark_idol/<int:idol_id>/", views.bookmark_idol_view, name="bookmark_idol"
    ),
    path(
        "bookmark_group/<int:group_id>/",
        views.bookmark_group_view,
        name="bookmark_group",
    ),
    path("idols/<int:idol_id>/", views.idol_detail_view, name="idol_detail"),
    path(
        "add_user_schedule/<int:schedule_id>/",
        views.add_user_schedule_view,
        name="add_user_schedule",
    ),
    path("my_schedules/", views.my_schedules_view, name="my_schedules"),
    path("remove_user_schedule/<int:user_schedule_id>/", views.remove_user_schedule_view, name="remove_user_schedule"),
    path("manager_schedule_test/", views.manager_schedule_test_view, name="manager_schedule_test"),
    path("add_schedule/", views.add_schedule_view, name="add_schedule"),
    path("idol_mainboard/", views.idol_mainboard_view, name="idol_mainboard"),
    path("manager_mainboard/", views.manager_mainboard_view, name="manager_mainboard"),
    path("fan_favorites/", views.fan_favorites_view, name="fan_favorites"),
]
