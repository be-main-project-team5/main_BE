from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import get_object_or_404, redirect, render

from apps.bookmarks.models import GroupBookmark, IdolBookmark
from apps.groups.models import Group
from apps.idols.models import Idol, IdolManager
from apps.schedules.models import IdolSchedule, GroupSchedule, UserSchedule # IdolSchedule과 UserSchedule의 새로운 경로
from apps.users.models import Image


def main(request):
    context = {
        "user": request.user,
        "user_profile_image_url": None,
    }

    if request.user.is_authenticated:
        if request.user.profile_image:
            context["user_profile_image_url"] = request.user.profile_image.image_file.url

        if request.user.role == 'NORMAL':
            context["bookmarked_idols"] = IdolBookmark.objects.filter(
                user=request.user
            ).select_related("idol")
            context["bookmarked_groups"] = GroupBookmark.objects.filter(
                user=request.user
            ).select_related("group")
            context["user_schedules"] = UserSchedule.objects.filter(user=request.user).select_related('idol_schedule__idol', 'group_schedule__group')

        elif request.user.role == 'IDOL':
            try:
                idol_instance = Idol.objects.get(user=request.user)
                context["my_idol_info"] = idol_instance
                context["my_idol_schedules"] = IdolSchedule.objects.filter(idol=idol_instance).order_by('start_time')
            except Idol.DoesNotExist:
                context["my_idol_info"] = None
                context["my_idol_schedules"] = []

        elif request.user.role == 'MANAGER':
            managed_idols = IdolManager.objects.filter(user=request.user).select_related('idol')
            context["managed_idols"] = managed_idols
            managed_idol_schedules = []
            for manager_entry in managed_idols:
                schedules = IdolSchedule.objects.filter(idol=manager_entry.idol).order_by('start_time')
                managed_idol_schedules.extend(schedules)
            context["managed_idol_schedules"] = managed_idol_schedules

        elif request.user.role == 'ADMIN':
            context["total_users"] = get_user_model().objects.count()
            context["total_idols"] = Idol.objects.count()
            context["total_groups"] = Group.objects.count()

    return render(
        request,
        "test_app/main.html",
        context,
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

        # If the user's role is 'IDOL', create an associated Idol instance
        if user.role == 'IDOL':
            # Assuming 'name' for Idol can be the same as user's nickname
            # 'group' can be left as None or set to a default if applicable
            Idol.objects.create(user=user, name=user.nickname, group=None) # group=None으로 설정

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
        user = authenticate(request, username=email, password=password)
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

from django.http import HttpResponseForbidden

def add_schedule_view(request):
    if not request.user.is_authenticated or request.user.role != 'MANAGER':
        return HttpResponseForbidden("접근 권한이 없습니다.")

    if request.method == 'POST':
        idol_id = request.POST.get('idol')
        title = request.POST.get('title')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        location = request.POST.get('location')
        description = request.POST.get('description')

        idol = get_object_or_404(Idol, id=idol_id)

        # Check if the manager is authorized to manage this idol
        if not IdolManager.objects.filter(user=request.user, idol=idol).exists():
            return HttpResponseForbidden("이 아이돌의 스케줄을 등록할 권한이 없습니다.")

        IdolSchedule.objects.create(
            idol=idol,
            manager=request.user,
            title=title,
            start_time=start_time,
            end_time=end_time,
            location=location,
            description=description
        )

    return redirect('main')

def my_schedules_view(request):
    if not request.user.is_authenticated:
        return redirect("/test/login/")

    user_schedules = UserSchedule.objects.filter(user=request.user).select_related('idol_schedule__idol', 'group_schedule__group')

    return render(
        request, "test_app/my_schedules.html", {"user": request.user, "user_schedules": user_schedules}
    )

def manager_schedule_test_view(request):
    test_results = []
    client = APIClient()
    User = get_user_model()

    # 1. 테스트용 매니저 및 아이돌 생성
    try:
        manager_user, created = User.objects.get_or_create(
            email="test_manager@example.com",
            defaults={'nickname': 'TestManager', 'role': 'MANAGER'}
        )
        if created:
            manager_user.set_password("testpassword")
            manager_user.save()
            test_results.append("테스트 매니저 계정 생성: 성공")
        else:
            test_results.append("테스트 매니저 계정 이미 존재.")

        idol_user, created = User.objects.get_or_create(
            email="test_idol@example.com",
            defaults={'nickname': 'TestIdol', 'role': 'IDOL'}
        )
        if created:
            idol_user.set_password("testpassword")
            idol_user.save()
            test_results.append("테스트 아이돌 계정 생성: 성공")
        else:
            test_results.append("테스트 아이돌 계정 이미 존재.")

        test_idol, created = Idol.objects.get_or_create(
            user=idol_user,
            defaults={'name': 'TestIdol', 'group': None}
        )
        if created:
            test_results.append("테스트 Idol 인스턴스 생성: 성공")
        else:
            test_results.append("테스트 Idol 인스턴스 이미 존재.")

        idol_manager, created = IdolManager.objects.get_or_create(
            user=manager_user,
            idol=test_idol
        )
        if created:
            test_results.append("IdolManager 관계 설정: 성공")
        else:
            test_results.append("IdolManager 관계 이미 존재.")

    except Exception as e:
        test_results.append(f"테스트 데이터 생성 중 오류 발생: {e}")
        return render(request, "test_app/manager_schedule_test.html", {"test_results": test_results})

    # 2. 매니저 로그인
    login_data = {'email': 'test_manager@example.com', 'password': 'testpassword'}
    login_response = client.post('/api/v1/users/login/', login_data, format='json')
    if login_response.status_code == status.HTTP_200_OK:
        test_results.append("매니저 로그인: 성공")
        access_token = login_response.data['access_token']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    else:
        try:
            error_detail = login_response.json()
        except Exception:
            error_detail = login_response.content.decode('utf-8')
        test_results.append(f"매니저 로그인 실패: {login_response.status_code} - {error_detail}")
        return render(request, "test_app/manager_schedule_test.html", {"test_results": test_results})

    # 3. 스케줄 생성 테스트
    schedule_data = {
        'idol': test_idol.id,
        'title': '테스트 스케줄',
        'start_time': timezone.now().isoformat(),
        'end_time': (timezone.now() + timedelta(hours=1)).isoformat(),
        'location': '테스트 장소',
        'description': '매니저가 생성한 테스트 스케줄',
        'is_public': True
    }
    create_response = client.post('/api/v1/schedules/idol_schedules/', schedule_data, format='json')
    if create_response.status_code == status.HTTP_201_CREATED:
        test_results.append(f"스케줄 생성: 성공 - {create_response.data}")
        created_schedule_id = create_response.data['id']
    else:
        test_results.append(f"스케줄 생성 실패: {create_response.status_code} - {create_response.data}")
        created_schedule_id = None

    # 4. 스케줄 조회 테스트 (매니저가 담당하는 아이돌 스케줄만 보여야 함)
    list_response = client.get('/api/v1/schedules/idol_schedules/')
    if list_response.status_code == status.HTTP_200_OK:
        test_results.append(f"스케줄 조회: 성공 - {list_response.data}")
        if created_schedule_id and any(s['id'] == created_schedule_id for s in list_response.data):
            test_results.append("생성된 스케줄이 조회 목록에 포함됨: 확인")
        else:
            test_results.append("생성된 스케줄이 조회 목록에 포함되지 않음: 오류")
    else:
        test_results.append(f"스케줄 조회 실패: {list_response.status_code} - {list_response.data}")

    # 5. 스케줄 수정 테스트
    if created_schedule_id:
        update_data = {'title': '수정된 테스트 스케줄', 'location': '수정된 장소'}
        update_response = client.patch(f'/api/v1/schedules/idol_schedules/{created_schedule_id}/', update_data, format='json')
        if update_response.status_code == status.HTTP_200_OK:
            test_results.append(f"스케줄 수정: 성공 - {update_response.data}")
        else:
            test_results.append(f"스케줄 수정 실패: {update_response.status_code} - {update_response.data}")

    # 6. 스케줄 삭제 테스트
    if created_schedule_id:
        delete_response = client.delete(f'/api/v1/schedules/idol_schedules/{created_schedule_id}/')
        if delete_response.status_code == status.HTTP_204_NO_CONTENT:
            test_results.append("스케줄 삭제: 성공")
        else:
            test_results.append(f"스케줄 삭제 실패: {delete_response.status_code} - {delete_response.data}")

    return render(request, "test_app/manager_schedule_test.html", {"test_results": test_results})
