from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import get_object_or_404, redirect, render

from apps.bookmarks.models import GroupBookmark, IdolBookmark
from apps.groups.models import Group
from apps.idols.models import Idol, IdolSchedule
from apps.users.models import Image, UserSchedule


def main(request):
    bookmarked_idols = []
    bookmarked_groups = []
    if request.user.is_authenticated:
        bookmarked_idols = IdolBookmark.objects.filter(
            user=request.user
        ).select_related("idol")
        bookmarked_groups = GroupBookmark.objects.filter(
            user=request.user
        ).select_related("group")

    user_profile_image_url = None
    if request.user.is_authenticated and request.user.profile_image:
        user_profile_image_url = request.user.profile_image.image_file.url

    return render(
        request,
        "test_app/main.html",
        {
            "user": request.user,
            "bookmarked_idols": bookmarked_idols,
            "bookmarked_groups": bookmarked_groups,
            "user_profile_image_url": user_profile_image_url,
        },
    )


def signup(request):
    if request.method == "POST":
        User = get_user_model()
        email = request.POST.get("email")
        nickname = request.POST.get("nickname")
        password = request.POST.get("password")
        role = request.POST.get("role")

        if User.objects.filter(email=email).exists():
            return render(
                request,
                "test_app/signup.html",
                {"error": "이미 존재하는 이메일입니다."},
            )
        if User.objects.filter(nickname=nickname).exists():
            return render(
                request,
                "test_app/signup.html",
                {"error": "이미 존재하는 닉네임입니다."},
            )

        user = User.objects.create_user(
            email=email, nickname=nickname, password=password, role=role
        )

        return render(
            request,
            "test_app/signup.html",
            {"message": f"{user.nickname}님, 회원가입이 완료되었습니다."},
        )

    return render(request, "test_app/signup.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("/test/")
        else:
            return render(
                request,
                "test_app/login.html",
                {"error": "이메일 또는 비밀번호가 올바르지 않습니다."},
            )
    return render(request, "test_app/login.html")


def logout_view(request):
    logout(request)
    return redirect("/test/")


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect("/test/login/")

    if request.method == "POST":
        if "profile_image" in request.FILES:
            uploaded_file = request.FILES["profile_image"]
            # 기존 이미지 삭제 (선택 사항)
            if request.user.profile_image:
                request.user.profile_image.delete()

            # 새 Image 객체 생성 및 저장
            new_image = Image(image_file=uploaded_file)
            new_image.save()

            # 사용자 프로필 이미지 업데이트
            request.user.profile_image = new_image
            request.user.save()
            return redirect("/test/profile/")

    return render(request, "test_app/profile.html", {"user": request.user})


def idol_list_view(request):
    if not request.user.is_authenticated:
        return redirect("/test/login/")

    idols = Idol.objects.all()
    for idol in idols:
        idol.is_bookmarked = IdolBookmark.objects.filter(
            user=request.user, idol=idol
        ).exists()

    return render(
        request, "test_app/idol_list.html", {"idols": idols, "user": request.user}
    )


def group_list_view(request):
    if not request.user.is_authenticated:
        return redirect("/test/login/")

    groups = Group.objects.all()
    for group in groups:
        group.is_bookmarked = GroupBookmark.objects.filter(
            user=request.user, group=group
        ).exists()

    return render(
        request, "test_app/group_list.html", {"groups": groups, "user": request.user}
    )


def bookmark_idol_view(request, idol_id):
    if not request.user.is_authenticated:
        return redirect("/test/login/")

    idol = get_object_or_404(Idol, id=idol_id)
    action = request.POST.get("action")

    if action == "add":
        IdolBookmark.objects.get_or_create(user=request.user, idol=idol)
    elif action == "remove":
        IdolBookmark.objects.filter(user=request.user, idol=idol).delete()

    return redirect("/test/idols/")


def bookmark_group_view(request, group_id):
    if not request.user.is_authenticated:
        return redirect("/test/login/")

    group = get_object_or_404(Group, id=group_id)
    action = request.POST.get("action")

    if action == "add":
        GroupBookmark.objects.get_or_create(user=request.user, group=group)
    elif action == "remove":
        GroupBookmark.objects.filter(user=request.user, group=group).delete()

    return redirect("/test/groups/")


def idol_detail_view(request, idol_id):
    if not request.user.is_authenticated:
        return redirect("/test/login/")

    idol = get_object_or_404(Idol, id=idol_id)
    schedules = idol.schedules.all()

    for schedule in schedules:
        schedule.is_added_to_user_schedule = UserSchedule.objects.filter(
            user=request.user, idol_schedule=schedule
        ).exists()

    return render(
        request, "test_app/idol_detail.html", {"idol": idol, "user": request.user}
    )


def add_user_schedule_view(request, schedule_id):
    if not request.user.is_authenticated:
        return redirect("/test/login/")

    schedule = get_object_or_404(IdolSchedule, id=schedule_id)
    action = request.POST.get("action")

    if action == "add":
        UserSchedule.objects.get_or_create(user=request.user, idol_schedule=schedule)
    elif action == "remove":
        UserSchedule.objects.filter(user=request.user, idol_schedule=schedule).delete()

    return redirect("/test/idols/" + str(schedule.idol.id) + "/")
