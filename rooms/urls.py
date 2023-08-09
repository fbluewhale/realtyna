from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import RoomsViewSet
from .views import    RoomsViewSet

router = DefaultRouter()
router.register(r"room", RoomsViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
