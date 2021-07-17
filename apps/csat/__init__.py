from django.db.models import TextChoices


class QuestionType(TextChoices):
    INPUT = "INPUT", "Произвольный текст"
    SELECT = "SELECT", "Выпадающий список"
    RADIO = "RADIO", "Один выбор"
    CHECKED = "CHECKED", "Множественный выбор"