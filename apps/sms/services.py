import logging
from datetime import timedelta
from random import random, randrange
from typing import Tuple, Union
from django.conf import settings
from django.db import transaction
from django.utils import timezone

from .models import SMSMessage
from .tasks import send_sms_task


def send_sms(
        recipient: str,
        message: str = "",
        kwargs=None,
):
    if kwargs is None:
        kwargs = {}

    message = message.format(**kwargs)

    send_sms_after = randrange(settings.SEND_SMS_FROM_MINUTES, settings.SEND_SMS_TO_MINUTES)
    sending_time = timezone.localtime() + timedelta(minutes=send_sms_after)
    with transaction.atomic():
        print(f"recipient_number: {recipient}, message: {message}, sending_time: {sending_time}")
        sms = SMSMessage(
            recipients=recipient, content=message, sending_time=sending_time,
        )
        sms.save()

        transaction.on_commit(
            lambda: send_sms_task.apply_async(
                eta=sending_time, args=[recipient, message, sms.uuid]
            )
        )