from django.contrib import admin

# Register your models here.
from apps.csat.models import ApplicationForm, ApplicationQuestion



class ApplicationQuestionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "question",
        "type",
        "application",
    )
    ordering = ("-created_at",)

admin.site.register(ApplicationForm)
admin.site.register(ApplicationQuestion, ApplicationQuestionAdmin)