from django.db import models
try:
    from django.db.models import JSONField
except ImportError:
    from django.contrib.postgres.fields import JSONField
# Create your models here.
from apps.core.models import TimestampModel
from apps.reports.storage import private_report_storage
from apps.users.models import User


class ReportFile(TimestampModel):
    class Meta:
        verbose_name = "Отчет"
        verbose_name_plural = "Отчеты"

    id = models.UUIDField(primary_key=True)
    file = models.FileField(storage=private_report_storage)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    filter_types = JSONField(null=True)

    def __str__(self):
        return f"{self.id} ({self.created_at_pretty})"