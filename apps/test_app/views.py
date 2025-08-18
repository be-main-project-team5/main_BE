from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse
from datetime import timedelta
from urllib.parse import urlencode

import requests
import json

from rest_framework.test import APIClient
from rest_framework import status

from apps.bookmarks.models import GroupBookmark, IdolBookmark
from apps.groups.models import Group
from apps.idols.models import Idol, IdolManager
from apps.schedules.models import IdolSchedule, GroupSchedule, UserSchedule
from apps.users.models import Image, CustomUser


def index(request):
    """로그인 페이지"""
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            api_login_url = request.build_absolute_uri('/api/v1/users/login/')
            try:
                api_response = requests.post(api_login_url, json={'email': email, 'password': password})
                api_response.raise_for_status()
                tokens = api_response.json()
            except requests.exceptions.RequestException:
                logout(request)
                return render(request, "test_app/index.html", {"error": "API 로그인에 실패했습니다."})

            if user.role == 'ADMIN': response = redirect('test_admin_main')
            elif user.role == 'MANAGER': response = redirect('manager_mainboard')
            elif user.role == 'IDOL': response = redirect('idol_mainboard')
            else: response = redirect('fan_favorites')

            response.set_cookie('access_token', tokens.get('access_token'))
            response.set_cookie('refresh_token', tokens.get('refresh_token'))
            return response
        else:
            return render(request, "test_app/index.html", {"error": "이메일 또는 비밀번호가 올바르지 않습니다."})

    if request.user.is_authenticated:
        return render(request, "test_app/main.html")

    context = {
        "kakao_rest_api_key": settings.KAKAO_REST_API_KEY,
        "kakao_redirect_uri": settings.KAKAO_REDIRECT_URI,
        "google_client_id": settings.GOOGLE_CLIENT_ID,
    }
    return render(request, "test_app/index.html", context)

def get_api_data(request, url):
    access_token = request.COOKIES.get('access_token')
    if not access_token: return None
    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API call failed: {e}")
        return None

def signup(request):
    if request.method == "POST":
        User, email, nickname, password, role = get_user_model(), request.POST.get("email"), request.POST.get("nickname"), request.POST.get("password"), request.POST.get("role")
        if User.objects.filter(email=email).exists(): return render(request, "test_app/signup.html", {"error": "이미 존재하는 이메일입니다."})
        if User.objects.filter(nickname=nickname).exists(): return render(request, "test_app/signup.html", {"error": "이미 존재하는 닉네임입니다."})
        user = User.objects.create_user(email=email, nickname=nickname, password=password, role=role)
        if user.role == 'IDOL': Idol.objects.create(user=user, name=user.nickname, group=None)
        return render(request, "test_app/signup.html", {"message": f"{user.nickname}님, 회원가입이 완료되었습니다."})
    return render(request, "test_app/signup.html")

def logout_view(request):
    access_token, refresh_token = request.COOKIES.get('access_token'), request.COOKIES.get('refresh_token')
    if refresh_token:
        api_logout_url = request.build_absolute_uri('/api/v1/users/logout/')
        headers = {'Authorization': f'Bearer {access_token}'}
        try: requests.post(api_logout_url, headers=headers)
        except requests.exceptions.RequestException as e: print(f"API logout failed: {e}")
    logout(request)
    response = redirect('index')
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response

def profile_view(request):
    if not request.user.is_authenticated: return redirect("index")
    if request.method == "POST" and "profile_image" in request.FILES:
        if request.user.profile_image: request.user.profile_image.delete()
        new_image = Image.objects.create(image_file=request.FILES["profile_image"])
        request.user.profile_image = new_image
        request.user.save()
        return redirect("profile")
    return render(request, "test_app/profile.html", {"user": request.user})

def idol_list_view(request):
    if not request.user.is_authenticated: return redirect("index")
    search_query = request.GET.get('search', '')
    idols = Idol.objects.filter(name__icontains=search_query) if search_query else Idol.objects.all()
    for idol in idols: idol.is_bookmarked = IdolBookmark.objects.filter(user=request.user, idol=idol).exists()
    return render(request, "test_app/idol_list.html", {"idols": idols, "search_query": search_query})

def group_list_view(request):
    if not request.user.is_authenticated: return redirect("index")
    groups = Group.objects.all()
    for group in groups: group.is_bookmarked = GroupBookmark.objects.filter(user=request.user, group=group).exists()
    return render(request, "test_app/group_list.html", {"groups": groups})

def idol_detail_view(request, idol_id):
    if not request.user.is_authenticated: return redirect("index")
    idol = get_object_or_404(Idol, id=idol_id)
    schedules = idol.schedules.all()
    for schedule in schedules: schedule.is_added_to_user_schedule = UserSchedule.objects.filter(user=request.user, idol_schedule=schedule).exists()
    return render(request, "test_app/idol_detail.html", {"idol": idol, "schedules": schedules})

def my_schedules_view(request):
    if not request.user.is_authenticated: return redirect("index")
    user_schedules = UserSchedule.objects.filter(user=request.user).select_related('idol_schedule__idol', 'group_schedule__group')
    return render(request, "test_app/my_schedules.html", {"user_schedules": user_schedules})

def bookmark_idol_view(request, idol_id):
    if not request.user.is_authenticated: return JsonResponse({'status': 'error', 'message': '로그인이 필요합니다.'}, status=401)
    if request.method == 'POST':
        idol = get_object_or_404(Idol, id=idol_id)
        action = request.POST.get("action")
        if action == "add":
            IdolBookmark.objects.get_or_create(user=request.user, idol=idol)
            return JsonResponse({'status': 'success', 'action': 'added', 'idol_id': idol_id})
        elif action == "remove":
            IdolBookmark.objects.filter(user=request.user, idol=idol).delete()
            return JsonResponse({'status': 'success', 'action': 'removed', 'idol_id': idol_id})
    return JsonResponse({'status': 'error', 'message': '잘못된 요청입니다.'}, status=400)

def bookmark_group_view(request, group_id):
    if not request.user.is_authenticated: return JsonResponse({'status': 'error', 'message': '로그인이 필요합니다.'}, status=401)
    if request.method == 'POST':
        group = get_object_or_404(Group, id=group_id)
        action = request.POST.get("action")
        if action == "add":
            GroupBookmark.objects.get_or_create(user=request.user, group=group)
            return JsonResponse({'status': 'success', 'action': 'added', 'group_id': group_id})
        elif action == "remove":
            GroupBookmark.objects.filter(user=request.user, group=group).delete()
            return JsonResponse({'status': 'success', 'action': 'removed', 'group_id': group_id})
    return JsonResponse({'status': 'error', 'message': '잘못된 요청입니다.'}, status=400)

def add_user_schedule_view(request, schedule_id):
    if not request.user.is_authenticated: return JsonResponse({'status': 'error', 'message': '로그인이 필���합니다.'}, status=401)
    if request.method == 'POST':
        schedule = get_object_or_404(IdolSchedule, id=schedule_id)
        action = request.POST.get("action")
        if action == "add":
            UserSchedule.objects.get_or_create(user=request.user, idol_schedule=schedule)
            return JsonResponse({'status': 'success', 'action': 'added', 'schedule_id': schedule_id})
        elif action == "remove":
            UserSchedule.objects.filter(user=request.user, idol_schedule=schedule).delete()
            return JsonResponse({'status': 'success', 'action': 'removed', 'schedule_id': schedule_id})
    return JsonResponse({'status': 'error', 'message': '잘못된 요청입니다.'}, status=400)

def fan_favorites_view(request):
    if not request.user.is_authenticated or request.user.role != 'NORMAL': return redirect("index")
    today = timezone.now().date()
    bookmarked_idols = IdolBookmark.objects.filter(user=request.user).select_related("idol")
    bookmarked_groups = GroupBookmark.objects.filter(user=request.user).select_related("group")

    idol_schedules = IdolSchedule.objects.filter(idol__in=[b.idol for b in bookmarked_idols])
    group_schedules = GroupSchedule.objects.filter(group__in=[b.group for b in bookmarked_groups])

    all_schedules = list(idol_schedules) + list(group_schedules)
    today_schedules = [s for s in all_schedules if s.start_time.date() == today]
    monthly_schedules = [s for s in all_schedules if s.start_time.year == today.year and s.start_time.month == today.month]

    monthly_schedules.sort(key=lambda s: s.start_time)
    today_schedules.sort(key=lambda s: s.start_time)

    context = {
        'bookmarked_idols': bookmarked_idols,
        'bookmarked_groups': bookmarked_groups,
        "today_schedules": today_schedules,
        "monthly_schedules": monthly_schedules,
    }
    return render(request, "test_app/fan_favorites.html", context)

def idol_mainboard_view(request):
    if not request.user.is_authenticated or request.user.role != 'IDOL': return redirect("index")
    today = timezone.now().date()
    all_schedules, today_schedules, monthly_schedules = [], [], []
    try:
        idol_instance = Idol.objects.select_related('group').get(user=request.user)
        idol_schedules = IdolSchedule.objects.filter(idol=idol_instance)
        for s in idol_schedules: s.schedule_type = '개인'
        all_schedules.extend(idol_schedules)
        if idol_instance.group:
            group_schedules = GroupSchedule.objects.filter(group=idol_instance.group)
            for s in group_schedules: s.schedule_type = '그룹'
            all_schedules.extend(group_schedules)
        
        for s in all_schedules:
            if s.start_time.date() == today:
                today_schedules.append(s)
            if s.start_time.year == today.year and s.start_time.month == today.month:
                monthly_schedules.append(s)
        
        monthly_schedules.sort(key=lambda s: s.start_time)
        today_schedules.sort(key=lambda s: s.start_time)

    except Idol.DoesNotExist: pass
    context = {"today_schedules": today_schedules, "monthly_schedules": monthly_schedules}
    return render(request, "test_app/idol_mainboard.html", context)

def manager_mainboard_view(request):
    if not request.user.is_authenticated or request.user.role != 'MANAGER': return redirect("index")
    today = timezone.now().date()
    managed_idols = IdolManager.objects.filter(user=request.user).select_related('idol__group')
    managed_idol_ids = [m.idol.id for m in managed_idols]
    
    idol_schedules = IdolSchedule.objects.filter(idol_id__in=managed_idol_ids)
    group_ids = [m.idol.group.id for m in managed_idols if m.idol.group]
    group_schedules = GroupSchedule.objects.filter(group_id__in=group_ids)

    all_schedules = list(idol_schedules) + list(group_schedules)
    today_schedules = [s for s in all_schedules if s.start_time.date() == today]
    monthly_schedules = [s for s in all_schedules if s.start_time.year == today.year and s.start_time.month == today.month]

    monthly_schedules.sort(key=lambda s: s.start_time)
    today_schedules.sort(key=lambda s: s.start_time)

    context = {
        "managed_idols": managed_idols,
        "today_schedules": today_schedules,
        "monthly_schedules": monthly_schedules,
        "all_groups": Group.objects.all(),
    }
    return render(request, "test_app/manager_mainboard.html", context)

@user_passes_test(lambda u: u.is_staff or u.role == 'MANAGER')
def add_schedule_view(request):
    if request.method == 'POST':
        schedule_type = request.POST.get('schedule_type')
        if schedule_type == 'idol':
            api_url = request.build_absolute_uri('/api/v1/schedules/idols/')
            data = {
                'idol': request.POST.get('idol_id'),
                'title': request.POST.get('title'),
                'start_time': request.POST.get('start_time'),
                'end_time': request.POST.get('end_time'),
                'location': request.POST.get('location'),
                'description': request.POST.get('description'),
            }
        elif schedule_type == 'group':
            api_url = request.build_absolute_uri('/api/v1/schedules/groups/')
            data = {
                'group': request.POST.get('group_id'),
                'title': request.POST.get('title'),
                'start_time': request.POST.get('start_time'),
                'end_time': request.POST.get('end_time'),
                'location': request.POST.get('location'),
                'description': request.POST.get('description'),
            }
        else:
            return redirect('manager_mainboard')

        headers = {'Authorization': f'Bearer {request.COOKIES.get("access_token")}'}
        try:
            response = requests.post(api_url, headers=headers, json=data, cookies=request.COOKIES)
            response.raise_for_status()
        except requests.exceptions.RequestException as e: print(f"API call failed: {e} - {response.text}")
    return redirect('manager_mainboard')

@user_passes_test(lambda u: u.is_staff or u.role == 'MANAGER')
def create_group_view(request):
    if request.method == 'POST':
        api_url = request.build_absolute_uri('/api/v1/groups/')
        headers = {'Authorization': f'Bearer {request.COOKIES.get("access_token")}'}
        data = {'name': request.POST.get('name'), 'debut_date': request.POST.get('debut_date'), 'agency': request.POST.get('agency')}
        try:
            response = requests.post(api_url, headers=headers, json=data, cookies=request.COOKIES)
            response.raise_for_status()
        except requests.exceptions.RequestException as e: print(f"API call failed: {e} - {response.text}")
    return redirect('manager_mainboard')

@user_passes_test(lambda u: u.is_staff or u.role == 'MANAGER')
def update_idol_group_view(request, idol_id):
    if request.method == 'POST':
        api_url = request.build_absolute_uri(f'/api/v1/idols/{idol_id}/update-group/')
        headers = {'Authorization': f'Bearer {request.COOKIES.get("access_token")}'}
        group_id = request.POST.get('group_id')
        data = {'group': int(group_id) if group_id else None}
        try:
            response = requests.patch(api_url, headers=headers, json=data, cookies=request.COOKIES)
            response.raise_for_status()
        except requests.exceptions.RequestException as e: print(f"API call failed: {e} - {response.text}")
    return redirect('manager_mainboard')

@user_passes_test(lambda u: u.is_staff)
def admin_mainboard_view(request):
    params = {k: v for k, v in request.GET.items() if v}
    base_url = request.build_absolute_uri('/api/v1/admins/users/')
    user_list_url = f"{base_url}?{urlencode(params)}" if params else base_url
    all_users = []
    page_url = user_list_url
    while page_url:
        api_data = get_api_data(request, page_url)
        if api_data and 'results' in api_data:
            all_users.extend(api_data['results'])
            page_url = api_data.get('next')
        else: break
    
    # 담당 관계 관리를 위한 데이터 추가
    all_managers = CustomUser.objects.filter(role='MANAGER')
    all_idols = Idol.objects.select_related('group').all()
    all_groups = Group.objects.all()
    manager_assignments = IdolManager.objects.select_related('user', 'idol').all()

    context = {
        'user_list': all_users, 
        'current_role_filter': request.GET.get('role'), 
        'current_search': request.GET.get('search'), 
        'current_ordering': request.GET.get('ordering'),
        'all_managers': all_managers,
        'all_idols': all_idols,
        'all_groups': all_groups,
        'manager_assignments': manager_assignments,
    }
    return render(request, "test_app/admin_mainboard.html", context)

@user_passes_test(lambda u: u.is_staff)
def admin_create_manager_view(request):
    if request.method == 'POST':
        api_url = request.build_absolute_uri('/api/v1/admins/create-manager/')
        headers = {'Authorization': f'Bearer {request.COOKIES.get("access_token")}'}
        data = {'password': request.POST.get('password'), 'email': request.POST.get('email'), 'nickname': request.POST.get('nickname')}
        try: 
            response = requests.post(api_url, headers=headers, json=data, cookies=request.COOKIES)
            response.raise_for_status()
        except requests.exceptions.RequestException as e: print(f"API call failed: {e} - {response.text}")
    return redirect('test_admin_main')

@user_passes_test(lambda u: u.is_staff)
def admin_delete_user_view(request, user_id):
    if request.method == 'POST':
        api_url = request.build_absolute_uri(f'/api/v1/admins/users/{user_id}/')
        headers = {'Authorization': f'Bearer {request.COOKIES.get("access_token")}'}
        try: 
            response = requests.delete(api_url, headers=headers, cookies=request.COOKIES)
            response.raise_for_status()
        except requests.exceptions.RequestException as e: print(f"API call failed: {e} - {response.text}")
    return redirect('test_admin_main')

@user_passes_test(lambda u: u.is_staff)
def admin_assign_manager_view(request):
    if request.method == 'POST':
        manager_id = request.POST.get('manager_id')
        idol_id = request.POST.get('idol_id')
        api_url = request.build_absolute_uri('/api/v1/admins/managers/')
        headers = {'Authorization': f'Bearer {request.COOKIES.get("access_token")}'}
        data = {'user': manager_id, 'idol': idol_id}
        try:
            response = requests.post(api_url, headers=headers, json=data, cookies=request.COOKIES)
            response.raise_for_status()
        except requests.exceptions.RequestException as e: print(f"API call failed: {e} - {response.text}")
    return redirect('test_admin_main')

@user_passes_test(lambda u: u.is_staff)
def admin_unassign_manager_view(request, assignment_id):
    if request.method == 'POST':
        api_url = request.build_absolute_uri(f'/api/v1/admins/managers/{assignment_id}/')
        headers = {'Authorization': f'Bearer {request.COOKIES.get("access_token")}'}
        try:
            response = requests.delete(api_url, headers=headers, cookies=request.COOKIES)
            response.raise_for_status()
        except requests.exceptions.RequestException as e: print(f"API call failed: {e} - {response.text}")
    return redirect('test_admin_main')

@user_passes_test(lambda u: u.is_staff)
def admin_update_idol_group_view(request, idol_id):
    if request.method == 'POST':
        api_url = request.build_absolute_uri(f'/api/v1/idols/{idol_id}/update-group/')
        headers = {'Authorization': f'Bearer {request.COOKIES.get("access_token")}'}
        group_id = request.POST.get('group_id')
        data = {'group': int(group_id) if group_id else None}
        try:
            response = requests.patch(api_url, headers=headers, json=data, cookies=request.COOKIES)
            response.raise_for_status()
        except requests.exceptions.RequestException as e: print(f"API call failed: {e} - {response.text}")
    return redirect('test_admin_main')

@user_passes_test(lambda u: u.is_staff)
def admin_create_idol_view(request):
    if request.method == 'POST':
        api_url = request.build_absolute_uri('/api/v1/admins/create-idol/')
        headers = {'Authorization': f'Bearer {request.COOKIES.get("access_token")}'}
        data = {'password': request.POST.get('password'), 'email': request.POST.get('email'), 'nickname': request.POST.get('nickname')}
        try: 
            response = requests.post(api_url, headers=headers, json=data, cookies=request.COOKIES)
            response.raise_for_status()
        except requests.exceptions.RequestException as e: print(f"API call failed: {e} - {response.text}")
    return redirect('test_admin_main')

def manager_schedule_test_view(request):
    # ... (This view is for isolated testing and remains unchanged) ...
    return render(request, "test_app/manager_schedule_test.html", {"test_results": []})
