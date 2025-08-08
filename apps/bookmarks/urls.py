from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GroupBookmarkViewSet, IdolBookmarkViewSet

router = DefaultRouter()
router.register(r"idols", IdolBookmarkViewSet)
router.register(r"groups", GroupBookmarkViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
