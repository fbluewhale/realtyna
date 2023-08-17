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

def handle_filter_reserved_room(start_date,end_date,**filters):
    filtered_data = ReservedRoom.objects.filter(
                checking_date__lte = end_date,
                checking_date__gte = start_date,
        ).all()
    filtered_data = filtered_data.filter(**filters) if filters else filtered_data
    return filtered_data

def handle_get_report_file(data:BookedRoomReportQuerySerializer):
        request_params_serializer = BookedRoomReportQuerySerializer(data=data)
        if request_params_serializer.is_valid():
            request_params_serializer = request_params_serializer.validated_data
            report = handle_filter_reserved_room(**request_params_serializer)
            serializer = ReservedRoomSerializer(report, many=True)
            return create_pdf_report(serializer, request_params_serializer)
        
def handle_get_report(data:BookedRoomReportQuerySerializer):
        request_params_serializer = BookedRoomReportQuerySerializer(data=data)
        if request_params_serializer.is_valid():
            request_params_serializer = request_params_serializer.validated_data
            report = handle_filter_reserved_room(**request_params_serializer)
            return report
