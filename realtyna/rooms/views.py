import datetime
import io
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from drf_yasg.utils import swagger_auto_schema
from utils.utils import validate_serializer
from booking.serializer import AvailableRoomSerializer
from booking.models import ReservedRoom

from .models import Room
from .serializer import RoomSerializer
from .serializer import RoomSerializer
from .helpers import handle_get_available_room

class RoomsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    This viewset automatically provides `list` actions.
    """

    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class AvailableRoomsViewSet(APIView, LimitOffsetPagination):
    # pagination_class = StandardResultsSetPagination

    @swagger_auto_schema(query_serializer=AvailableRoomSerializer)
    @validate_serializer(AvailableRoomSerializer)
    def get(self, request):
        available_room_query = handle_get_available_room(request.GET)
        available_room_query = self.paginate_queryset(
            available_room_query, request, view=self
        )
        serializer = RoomSerializer(available_room_query, many=True)
        return self.get_paginated_response(serializer.data)
