import datetime
import io
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.decorators import method_decorator
from django.http import FileResponse
from django.shortcuts import render
from django.http import FileResponse
from utils.serializers import StandardResultsSetPagination
from utils.utils import validate_serializer
from utils.exception import BadRequest
from .models import Room
from .models import ReservedRoom
from .serializer import RoomSerializer
from .serializer import (
    ReservedRoomSerializer,

    RoomSerializer,
)
from fpdf import FPDF


class RoomsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    This viewset automatically provides `list` actions.
    """

    queryset = Room.objects.all()
    serializer_class = RoomSerializer