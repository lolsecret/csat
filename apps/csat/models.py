from uuid import uuid4

from django.db import models
from django.utils import timezone

try:
    from django.db.models import JSONField
except ImportError:
    from django.contrib.postgres.fields import JSONField
from apps.core.models import TimestampModel
from apps.csat import QuestionType


class ApplicationForm(TimestampModel):
    uuid = models.UUIDField("Идентификатор", default=uuid4, unique=True, editable=False)
    date_of_published = models.DateField("Дата публикации", null=True, blank=True)
    is_expired = models.BooleanField("Проходить снова", default=False)

    def __str__(self):
        return f'{self.id}. Опросник, Дата публикации {self.date_of_published}'

    class Meta:
        verbose_name = "Опросник"
        verbose_name_plural = "Опросники"


class ApplicationQuestion(TimestampModel):
    application = models.ForeignKey(
        ApplicationForm,
        on_delete=models.CASCADE,
        verbose_name="Опросник",
        related_name="questions",
        null=True,
    )
    answer = JSONField("Ответ", max_length=255, null=True, editable=False)
    question = models.CharField("Вопрос", max_length=255)
    type = models.CharField(choices=QuestionType.choices, default=QuestionType.RADIO, max_length=255)

    def __str__(self):
        return f'{self.question}, {self.type}'

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"