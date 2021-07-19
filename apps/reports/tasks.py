import os
from datetime import timedelta, datetime
from typing import List, Union
from uuid import UUID
from urllib.parse import urljoin

from celery import shared_task, current_task, Task
from django.utils.timezone import localtime

from apps.core.tasks import BaseNotifyTask
from apps.csat.models import ApplicationForm, ApplicationQuestion
from apps.reports.models import ReportFile
from apps.reports.storage import private_report_storage
from apps.users.models import User
from online_store.celery import app
from django.conf import settings
from pyexcelerate import Workbook
from dateutil import tz

@app.task(
    name="notifications.notify_report_readiness",
    base=BaseNotifyTask,
    bind=True
)
def notify_report_readiness(
        self,
        report_uuid: UUID,
        success: bool = False
):
    url = urljoin(settings.WS_PUB_URL, str(report_uuid))

    response = self.session.post(url, json={"success": success})
    print(f"report uuid - {report_uuid}")

    return str(response.request.__dict__)


@shared_task
def remove_expired_report(report_uuid: UUID):
    try:
        report = ReportFile.objects.get(id=report_uuid)
        try:
            os.remove(report.file.path)
        except FileNotFoundError:
            pass
        report.delete()

    except ReportFile.DoesNotExist:
        print(f"Report file ({report_uuid}) does not exist")


class GenerateReportTask(Task):
    name = "internal_api.generate_mobile_report"
    sheet_name = "Отчет по СМС"

    def run(self, *args, **kwargs):
        row_num = 1
        user = User.objects.get(id=1)
        filter_types = {
            "created_at_begin": kwargs.get("created_at_begin"),
            "created_at_end": kwargs.get("created_at_end")
        }

        workbook: Workbook = Workbook()
        worksheet = workbook.new_sheet(self.sheet_name)
        worksheet.range("A1", "AC1").value = [self.get_columns()]

        application_question = self.get_queryset(kwargs)
        print(f"Generate report task({current_task.request.id})")

        for question in application_question:
            try:
                row = self.get_rows(question=question)
                row_num += 1
                for col_num, cell_value in enumerate(row, 1):
                    worksheet.set_cell_value(row_num, col_num, cell_value)
                else:
                    continue

            except AttributeError as exc:
                print(
                    f"Generate report task ({current_task.request.id})"
                )

        filename = f"{localtime().strftime('%Y-%m-%d_%H-%M-%S')}-applications.xlsx"
        file_path = os.path.join(private_report_storage.location, filename)

        workbook.save(file_path)

        report: ReportFile = ReportFile.objects.create(
            id=current_task.request.id,
            file=filename,
            user=user,
            filter_types=filter_types
        )
        remove_date = localtime(report.created_at) + timedelta(hours=6)
        remove_expired_report.apply_async(
            (report.id,),
            eta=remove_date
        )

        return {"success": True, "file_url": report.id}

    @staticmethod
    def get_queryset(kwargs):
        created_at_begin = datetime.strptime(kwargs.get("created_at_begin"), "%Y-%m-%dT%H:%M:%S")
        created_at_end = datetime.strptime(kwargs.get("created_at_end"), "%Y-%m-%dT%H:%M:%S")

        tz_info = tz.gettz(settings.TIME_ZONE)
        start_of_day = datetime(created_at_begin.year, created_at_begin.month, created_at_begin.day, tzinfo=tz_info)
        end_of_day = datetime(
            created_at_end.year, created_at_end.month, created_at_end.day,
            hour=23, minute=59, second=59, tzinfo=tz_info
        )
        return ApplicationQuestion.objects.filter(
            changed_at__gte=start_of_day, changed_at__lte=end_of_day
        ).distinct()

    @staticmethod
    def get_columns() -> List[str]:
        return [
            "Дата и время предоставления ответа",
            "Оценка", "Скорость ответа",
        ]

    @staticmethod
    def get_rows(question: ApplicationQuestion) -> List[Union[str, int]]:

        return [
            question.date_answer,
            question.answer,
            question.time_to_answer
        ]


generate_report_task = app.register_task(GenerateReportTask())