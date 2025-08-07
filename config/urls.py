"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Django admin 사이트 URL
    path("admin/", admin.site.urls),
    path("api/v1/users/", include("apps.users.urls")),
# /api/v1/ 경로로 들어오는 요청은 apps.groups.urls에서 처리
    path("api/v1/idols/", include("apps.idols.urls")),
    # /api/v1/ 경로로 들어오는 요청은 apps.groups.urls에서 처리
    path("api/v1/groups/", include("apps.groups.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
