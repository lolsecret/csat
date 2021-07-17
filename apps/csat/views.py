from django.conf import settings
from django.shortcuts import render
from django.utils import timezone
from rest_framework import status

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.csat.models import ApplicationForm
from apps.csat.serializers import ApplyApplicationSerializer, ApplicationApplyFormSerializers, \
    ApplicationFormRequestSerializer
from apps.sms.models import SMSMessage
from apps.sms.services import send_sms
from apps.users.models import User


def get_application(queryset):
    print(f'query: {queryset}')
    return queryset.filter(is_expired=True, date_of_published__lte=timezone.localtime()).first()


class ApplyApplicationView(GenericAPIView):
    serializer_class = ApplicationApplyFormSerializers
    queryset = ApplicationForm.objects.all()
    def post(self, request, *args, **kwargs):
        serializer = ApplyApplicationSerializer(data=request.data)
        serializer.is_valid()

        application = get_application(self.queryset)
        mobile_phone = request.data['mobile_phone']
        person = User.objects.filter(id=request.data['person_id'])

        sms = SMSMessage.objects.filter(recipients=mobile_phone)

        if sms.exists():
            if sms.first().check_frequency_of_sending_sms:
                send_sms(
                    recipient=str(mobile_phone),
                    message=settings.SMS_SENDING_MESSAGE
                )
        else:
            send_sms(
                recipient=str(mobile_phone),
                message=settings.SMS_SENDING_MESSAGE
            )
        return Response(
            data=self.serializer_class(instance=application).data,
            status=status.HTTP_200_OK
        )


class ApplicationFormView(GenericAPIView):
    queryset = ApplicationForm
    def post(self, request, *args, **kwargs):
        serializer = ApplicationFormRequestSerializer(data=request.data, many=True)


        print(request.data)
        return Response(status=status.HTTP_200_OK)