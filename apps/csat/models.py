from uuid import uuid4

from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from apps.users.models import User

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
    answer = models.CharField("Ответ", max_length=255, null=True, editable=False)
    question = models.CharField("Вопрос", max_length=255)

    date_answer = models.DateTimeField("Дата и время предоставления ответа", null=True, editable=False)
    type = models.CharField(choices=QuestionType.choices, default=QuestionType.RADIO, max_length=255)
    time_to_answer = models.CharField("Время потраченное на ответ", null=True, max_length=20, editable=False)

    def __str__(self):
        return f'{self.question}, {self.type}'

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class AnswerOptions(TimestampModel):
    answer_option = models.CharField("Варианты ответов", null=True, blank=True, max_length=255)
    questions = models.ManyToManyField(
        ApplicationQuestion,
        verbose_name="Вопросы",
        related_name="answer_options",
    )

    def __str__(self):
        return f'{self.id}. {self.answer_option}'

    class Meta:
        verbose_name = "Варианты ответов"
        verbose_name_plural = "Варианты ответов"


class UserApplicationForm(TimestampModel):
    form = models.ForeignKey(
        ApplicationForm,
        on_delete=models.CASCADE,
        verbose_name="Опросник",
        related_name="user_forms",
        null=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="application_form",
        null=True,
    )

    def __str__(self):
        return f'Опросник #{self.form.id}. Пользователь - {self.user}'

    class Meta:
        verbose_name = "Настройка пользователя для опросника"
        verbose_name_plural = "Настройки пользователей для опросника"
