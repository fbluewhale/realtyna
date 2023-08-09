
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from django.shortcuts import render
from utils.serializers import StandardResultsSetPagination
from utils.utils import validate_serializer
from utils.exception import BadRequest
from .models import ReservedRoom
from .serializer import (
    ReservedRoomSerializer,
    CheckRoomIsAvailableSerializer,
    BookRoomSerializer,
)
from fpdf import FPDF




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
        # if room_is_available:
        request_params_serializer = CheckRoomIsAvailableSerializer(data=request.data)
        if request_params_serializer.is_valid():
            request_params_serializer = request_params_serializer.validated_data
            reserved_is_available = ReservedRoom.objects.filter(
                date=request_params_serializer.get("date"),
                room=request_params_serializer.get("room"),
            ).exists()
            booking_serializer = BookRoomSerializer(data=request.data)
            if not reserved_is_available and booking_serializer.is_valid():
                booking_serializer.create(booking_serializer.validated_data)
                return Response(booking_serializer.data, status=201)
            date = request_params_serializer.get("date")
            raise BadRequest(f"room is not available at {date}")

