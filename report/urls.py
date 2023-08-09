from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from .views import (
    GetBookingReport,
    GetBookingReportFile,
)


urlpatterns = [
    path("get_report/", GetBookingReport.as_view()),
    path("get_report_file/", GetBookingReportFile.as_view()),
]
