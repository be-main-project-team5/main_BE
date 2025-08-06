from django.contrib import admin
from .models import Group

# 이 파일은 Django 관리자(Admin) 사이트에 Group 모델을 등록하여
# 관리자가 웹 인터페이스를 통해 Group 데이터를 쉽게 관리(생성, 조회, 수정, 삭제)할 수 있도록 합니다.

# @admin.register(Group) 데코레이터는 Group 모델을 Django 관리자 사이트에 등록하는 역할을 합니다.
# GroupAdmin 클래스는 Group 모델의 관리자 페이지에서 어떻게 보이고 작동할지 정의합니다.
class GroupAdmin(admin.ModelAdmin):
    # list_display: 관리자 목록 페이지에 표시될 필드들을 지정합니다.
    # 여기에 나열된 필드들은 Group 객체 목록을 볼 때 테이블의 열로 나타납니다.
    # 이를 통해 관리자는 각 그룹의 주요 정보를 한눈에 파악할 수 있습니다.
    list_display = ('name', 'debut_date', 'agency', 'created_at', 'updated_at')

    # search_fields: 관리자 목록 페이지에서 검색 기능을 제공할 필드들을 지정합니다.
    # 여기에 지정된 필드들을 기준으로 검색이 가능해져, 특정 그룹을 쉽게 찾을 수 있습니다.
    search_fields = ('name', 'agency')
