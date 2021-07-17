from django.db import models

# Create your models here.
from django.utils.timezone import localtime


class TimestampModel(models.Model):
    created_at = models.DateTimeField(
        "Время создания", auto_now_add=True, db_index=True
    )
    changed_at = models.DateTimeField(
        "Время последнего изменения", auto_now=True, db_index=True
    )

    class Meta:
        abstract = True

    @property
    def created_at_pretty(self):
        return localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")

    @property
    def updated_at_pretty(self):
        return localtime(self.changed_at).strftime("%d.%m.%Y %H:%M:%S")
    created_at_pretty.fget.short_description = "Время создания"
    updated_at_pretty.fget.short_description = "Время последнего изменения"


class ChangeOnlyMixin:
    def has_add_permission(self, request, obj=None):
        return False


class ReadOnlyMixin(ChangeOnlyMixin):
    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False