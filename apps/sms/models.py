from datetime import timedelta
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils import timezone

try:
    from django.db.models import JSONField
except ImportError:
    from django.contrib.postgres.fields import JSONField
# Create your models here.
from django.utils.timezone import localtime

from apps.core.models import TimestampModel


class SMSMessage(TimestampModel):
    uuid = models.UUIDField("Идентификатор", default=uuid4, unique=True, editable=False)
    recipients = models.CharField("Получатель", max_length=255, editable=False)
    content = models.TextField("Содержимое", editable=False)
    sending_time = models.DateTimeField("Время отправки смс", null=True)
    error_code = models.IntegerField("Код ошибки", null=True, editable=False)
    error_description = models.CharField(
        "Описание ошибки", max_length=255, null=True, editable=False
    )

    @property
    def local_sending_time(self):
        return localtime(self.sending_time).strftime("%d.%m.%Y %H:%M:%S")

    @property
    def check_frequency_of_sending_sms(self):
        if self.created_at + timedelta(days=settings.FREQUENCY_OF_SENDING_SMS) > timezone.localtime():
            return False
        return True

    class Meta:
        verbose_name = "SMS сообщение"
        verbose_name_plural = "SMS сообщения"