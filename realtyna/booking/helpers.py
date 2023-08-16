from rest_framework.response import Response
from django.db import transaction
from utils.exception import BadRequest
from rooms.models import Room
from .models import ReservedRoom
from .serializer import (
    CheckRoomIsAvailableSerializer,
    BookRoomSerializer,
)

def handle_reservation_room(data):
    # if room_is_available:
    request_params_serializer = CheckRoomIsAvailableSerializer(data=data)
    if request_params_serializer.is_valid():
        request_params_serializer = request_params_serializer.validated_data
        with transaction.atomic():
            #prevent the race condition 
            room = Room.objects.select_for_update().filter(id=request_params_serializer.get("room"))
            reserved_is_available = ReservedRoom.objects.select_for_update().filter(
                checking_date__lte=request_params_serializer.get("checking_date"),
                checkout_date__gte=request_params_serializer.get("checkout_date") ,
                room=request_params_serializer.get("room"),
            ).exists()
            booking_serializer = BookRoomSerializer(data=data)
            if not reserved_is_available and booking_serializer.is_valid()  and room.exists():
                booking_serializer.create(booking_serializer.validated_data)
                return Response(booking_serializer.data, status=201)
            date = request_params_serializer.get("date")
            raise BadRequest(f"room is not available at {date}")