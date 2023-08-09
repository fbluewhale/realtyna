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


class GetBookingReport(APIView, LimitOffsetPagination):
    @swagger_auto_schema(query_serializer=BookedRoomReportQuerySerializer)
    @validate_serializer(BookedRoomReportQuerySerializer)  # , method="GET")
    def get(self, request):
        request_params_serializer = BookedRoomReportQuerySerializer(data=request.GET)
        if request_params_serializer.is_valid():
            request_params_serializer = request_params_serializer.validated_data
            report = self.paginate_queryset(
                ReservedRoom.objects.filter(
                    date__range=[
                        request_params_serializer.get("start_date"),
                        request_params_serializer.get("end_date"),
                    ]
                ).all(),
                request,
                view=self,
            )
            serializer = ReservedRoomSerializer(report, many=True)
            return self.get_paginated_response(serializer.data)


class GetBookingReportFile(APIView, LimitOffsetPagination):
    @swagger_auto_schema(query_serializer=BookedRoomReportQuerySerializer)
    @validate_serializer(BookedRoomReportQuerySerializer)  # , method="GET")
    def get(self, request):
        request_params_serializer = BookedRoomReportQuerySerializer(data=request.GET)
        if request_params_serializer.is_valid():
            request_params_serializer = request_params_serializer.validated_data
            report = ReservedRoom.objects.filter(
                date__range=[
                    request_params_serializer.get("start_date"),
                    request_params_serializer.get("end_date"),
                ]
            ).all()
            serializer = ReservedRoomSerializer(report, many=True)
            return create_pdf_report(serializer, request_params_serializer)
