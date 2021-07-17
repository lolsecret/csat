from datetime import date
from dateutil.relativedelta import relativedelta
from rest_framework import serializers


class ReportFilterSerializer(serializers.Serializer):
    created_at_begin = serializers.DateField(default=date.today() - relativedelta(months=3))
    created_at_end = serializers.DateField(default=date.today())