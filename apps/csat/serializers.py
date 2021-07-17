from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from apps.csat.models import ApplicationQuestion, ApplicationForm, AnswerOptions


class AnswerOptionsSerializers(serializers.ModelSerializer):
    class Meta:
        model = AnswerOptions
        fields = (
            'id',
            'answer_option'
        )



class ApplicationQuestionSerializers(serializers.ModelSerializer):
    answer_options = AnswerOptionsSerializers(many=True)
    class Meta:
        model = ApplicationQuestion
        fields = (
            'id',
            'question',
            'type',
            'answer_options'
        )


class ApplicationApplyFormSerializers(serializers.ModelSerializer):
    questions = ApplicationQuestionSerializers(many=True)

    class Meta:
        model = ApplicationForm
        fields = (
            'uuid',
            'is_expired',
            'questions',
            'created_at'
        )


class ApplyApplicationSerializer(serializers.Serializer):
    person_id = serializers.IntegerField(label="ID пользователя")
    product = serializers.CharField(label="Название товара")
    mobile_phone = PhoneNumberField(
        required=True, write_only=True, label="Мобильный телефон"
    )


class ApplicationFormRequestSerializer(serializers.Serializer):
   question_id = serializers.IntegerField(label="ID вопроса")
   answer = serializers.JSONField(label="Ответ")
