from django.urls import path

from apps.reports.views import GenerateReport, DownloadReport

urlpatterns = [
    path("generate_report", GenerateReport.as_view()),
    path("download_report/<uuid:report_uuid>", DownloadReport.as_view()),
    ]