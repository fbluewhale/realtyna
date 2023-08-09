import datetime
import io
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Room
from .serializer import RoomSerializer
from .serializer import     RoomSerializer
from fpdf import FPDF


class RoomsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    This viewset automatically provides `list` actions.
    """

    queryset = Room.objects.all()
    serializer_class = RoomSerializer