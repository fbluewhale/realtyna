from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import mixins
from drf_yasg.utils import swagger_auto_schema
from utils.serializers import StandardResultsSetPagination
from utils.utils import validate_serializer
from .models import ReservedRoom
from .serializer import (
    ReservedRoomSerializer,
    BookRoomSerializer,
)
from .helpers import handle_reservation_room

class ReservedRoomsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    This viewset automatically provides `list` actions.
    """

    queryset = ReservedRoom.objects.all()
    serializer_class = ReservedRoomSerializer
    pagination_class = StandardResultsSetPagination


class BookingRoomsViewSet(APIView):
    """api view for book the room"""

    @swagger_auto_schema(request_body=BookRoomSerializer)
    @validate_serializer(BookRoomSerializer)  # , method="GET")
    def post(self, request):
        return handle_reservation_room(request.data)
