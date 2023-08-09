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
from fpdf import FPDF


class RoomsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    This viewset automatically provides `list` actions.
    """

    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class AvailableRoomsViewSet(APIView, LimitOffsetPagination):
    # pagination_class = StandardResultsSetPagination

    # @validate_serializer(AvailableRoomSerializer)
    @swagger_auto_schema(query_serializer=AvailableRoomSerializer)
    @validate_serializer(AvailableRoomSerializer)
    def get(self, request):
        request_params_serializer = AvailableRoomSerializer(data=request.GET)
        request_params_serializer = (
            request_params_serializer.is_valid()
            and request_params_serializer.validated_data
        )
        reserved_room_id = (
            ReservedRoom.objects.filter(date=request_params_serializer.get("date"))
            .all()
            .values("room")
        )
        available_room_query = Room.objects.exclude(id__in=reserved_room_id).all()
        available_room_query = self.paginate_queryset(
            available_room_query, request, view=self
        )
        serializer = RoomSerializer(available_room_query, many=True)
        return self.get_paginated_response(serializer.data)
