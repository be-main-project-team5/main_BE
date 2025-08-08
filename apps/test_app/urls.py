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
]
