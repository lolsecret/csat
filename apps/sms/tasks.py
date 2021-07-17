import xml.etree.ElementTree as ET
import requests
from django.conf import settings
from requests.exceptions import ConnectionError, HTTPError, Timeout, ReadTimeout

from online_store.celery import app
from .models import SMSMessage


@app.task(
    autoretry_for=(ConnectionError, HTTPError, Timeout),
    default_retry_delay=2,
    retry_kwargs={"max_retries": 5},
    ignore_result=True,
)
def send_sms_task(recipient: str, message: str, message_id: str):
    print(f"send_sms_task recipient: {recipient}")
    instance = SMSMessage.objects.get(uuid=message_id)
    try:
        response = requests.get(
            settings.SMS_API_URL,
            params={
                "login": settings.SMS_API_LOGIN,
                "password": settings.SMS_API_PASSWORD,
                "phones": recipient.replace('+', ''),
                "message": message,
                "rus": 5,
            },
            timeout=30,
            verify=False,
        )
        print(f"send_sms_task response.text: {response.text}")
        root = ET.fromstring(response.text)
        response_data = {}
        for r in root:
            response_data[r.tag] = r.text

        try:
            status_code = response_data.get("code")
            if "ERROR" in response_data['result']:
                instance.error_description = response_data.get("description")
                instance.error_code = status_code
        except AttributeError:
            instance.error_description = response.text
    except ReadTimeout as e:
        response_data = e.__str__()
        instance.error_description = response_data
    instance.save(update_fields=["error_description", "error_code"])
    return response_data
