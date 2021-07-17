from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from apps.csat.models import ApplicationQuestion


class ApplicationQuestionSerializers(serializers.ModelSerializer):
    class Meta:
        model = ApplicationQuestion
        fields = (
            'question',
            'type'
        )


class ApplicationFormSerializers(serializers.ModelSerializer):
    questions = ApplicationQuestionSerializers
    class Meta:
        fields = (
            'uuid',
            'is_expired',
            'questions',
        )


class ApplyApplicationSerializer(serializers.Serializer):
    person_id = serializers.CharField(label="ID пользователя")
    product = serializers.CharField(label="Название товара")
    mobile_phone = PhoneNumberField(
        required=True, write_only=True, label="Мобильный телефон"
    )