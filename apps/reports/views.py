import mimetypes
import os
from datetime import datetime, date

from django.http import FileResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework.views import APIView

from apps.reports.models import ReportFile
from apps.reports.serializers import ReportFilterSerializer
from apps.reports.tasks import notify_report_readiness, generate_report_task
from rest_framework.response import Response

class GenerateReport(APIView):

    # @swagger_auto_schema(request_body=ReportFilterSerializer)
    def post(self, request, *args, **kwargs):
        serializer = ReportFilterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        created_at_end = serializer.data.get("created_at_end")
        filter_types = {
            "created_at_begin": serializer.data.get("created_at_begin"),
            "created_at_end": created_at_end
        }

        report = ReportFile.objects.filter(filter_types=filter_types)
        if report.exists() and date.today() != datetime.strptime(created_at_end, "%Y-%m-%d").date():
            report = report.first()

            notify_report_readiness.delay(
                report_uuid=report.id,
                success=True
            )
            return Response({"report_uuid": report.id})

        task = generate_report_task.delay(
            user_id=request.user.id,
            **serializer.validated_data
        )

        return Response({"report_uuid": task.task_id})


class DownloadReport(APIView):

    def get(self, request, report_uuid):
        report = get_object_or_404(ReportFile, id=report_uuid)
        file = report.file
        file.open()
        filename = os.path.basename(file.name)
        file_expr = 'filename="{}"'.format(filename)

        content_type = mimetypes.guess_type(str(filename))[0]
        response = FileResponse(file)
        response["Content-Length"] = file.size

        response["Content-Type"] = content_type
        response["Content-Disposition"] = "attachment; {}".format(file_expr)

        return response