from django.contrib import admin

# Register your models here.
from apps.sms.models import SMSMessage
from apps.core.models import ReadOnlyMixin


class SMSMessageAdmin(ReadOnlyMixin, admin.ModelAdmin):
    list_display_links = "uuid",
    list_display = (
        "uuid",
        "get_sending_time",
        "has_delay",
        "recipients",
        "content",
        "error_code",
        "error_description",
    )
    readonly_fields = (
        "uuid",
        "recipients",
        "has_delay",
        "content",
        "get_sending_time",
        "error_code",
        "error_description",
    )
    ordering = ("-created_at",)
    search_fields = ("recipients", )

    def get_sending_time(self, obj):
        return obj.sending_time or obj.created_at

    def has_delay(self, obj):
        return bool(obj.sending_time)

    has_delay.boolean = True
    has_delay.short_description = "С задержкой"
    get_sending_time.short_description = "Время отправки"


admin.site.register(SMSMessage, SMSMessageAdmin)