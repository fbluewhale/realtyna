from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ReservedRoomsViewSet, BookingRoomsViewSet

router = DefaultRouter()
router.register(r"reserved_room", ReservedRoomsViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("booking_room/", BookingRoomsViewSet.as_view()),
]
