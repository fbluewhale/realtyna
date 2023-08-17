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
from django.shortcuts import render
from utils.utils import validate_serializer

from booking.models import ReservedRoom
from booking.serializer import (
    ReservedRoomSerializer,
    BookedRoomReportQuerySerializer,
)
from .utils import create_pdf_report
from .helpers import handle_get_report_file,handle_get_report

class GetBookingReport(APIView, LimitOffsetPagination):
    @swagger_auto_schema(query_serializer=BookedRoomReportQuerySerializer)
    @validate_serializer(BookedRoomReportQuerySerializer)  # , method="GET")
    def get(self, request):
        reports =  handle_get_report(request.GET)
        paginate_reports = self.paginate_queryset(reports, request,view=self)
        serializer = ReservedRoomSerializer(paginate_reports, many=True)
        return self.get_paginated_response(serializer.data)



class GetBookingReportFile(APIView, LimitOffsetPagination):
    @swagger_auto_schema(query_serializer=BookedRoomReportQuerySerializer)
    @validate_serializer(BookedRoomReportQuerySerializer)  # , method="GET")
    def get(self, request):
        return handle_get_report_file(request.GET)
