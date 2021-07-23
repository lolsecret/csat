from django.conf import settings
from django.shortcuts import render
from django.utils import timezone
from rest_framework import status

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.csat.models import ApplicationForm
from apps.csat.serializers import ApplyApplicationSerializer, ApplicationApplyFormSerializers, \
    ApplicationFormRequestSerializer
from apps.csat.utils import update_question
from apps.sms.models import SMSMessage
from apps.sms.services import send_sms
from apps.users.models import User


def get_application(queryset, user):
    return queryset.filter(is_expired=True, date_of_published__lte=timezone.localtime(), user_forms__user=user).first()


class ApplyApplicationView(GenericAPIView):
    serializer_class = ApplicationApplyFormSerializers
    queryset = ApplicationForm.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = ApplyApplicationSerializer(data=request.data)
        serializer.is_valid()

        user = User.objects.filter(id=request.data['person_id'])
        user.update(mobile_phone=request.data['mobile_phone'])

        application = get_application(self.queryset, user.first())
        mobile_phone = request.data['mobile_phone']


        sms = SMSMessage.objects.filter(recipients=mobile_phone)

        if sms.exists():
            print("Пользователю уже отправлялось сообщение")
            if sms.first().check_frequency_of_sending_sms:
                print("Проверка по времени отрправки пройдено. Отправляем смс...")
                send_sms(
                    recipient=str(mobile_phone),
                    message=settings.SMS_SENDING_MESSAGE
                )
        else:
            print("Пользователю еще не отправлялось сообщение. Отправляем смс сообщение...")
            send_sms(
                recipient=str(mobile_phone),
                message=settings.SMS_SENDING_MESSAGE
            )
        return Response(
            data=self.serializer_class(instance=application).data,
            status=status.HTTP_200_OK
        )


class ApplicationFormView(GenericAPIView):
    queryset = ApplicationForm.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = ApplicationFormRequestSerializer(data=request.data, many=True)
        serializer.is_valid()
        update_question(request.data)

        return Response(status=status.HTTP_200_OK)

