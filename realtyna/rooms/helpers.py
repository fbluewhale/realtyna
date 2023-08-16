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




def handle_get_available_room(data):
        request_params_serializer = AvailableRoomSerializer(data=data)
        request_params_serializer = (
            request_params_serializer.is_valid()
            and request_params_serializer.validated_data
        )
        reserved_room_id = (
            ReservedRoom.objects.filter(
                checking_date__lte=request_params_serializer.get("checking_date"),
                checkout_date__gte=request_params_serializer.get("checkout_date") ,
            )
            .all()
            .values("room")
        )
        available_room_query = Room.objects.exclude(id__in=reserved_room_id).all()
        return  available_room_query
