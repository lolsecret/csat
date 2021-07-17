from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _  # type: ignore

default_app_config = 'apps.users.apps.UsersConfig'


class RoleTypes(TextChoices):
    BUYER = 'BUYER', _('Покупатель')
    ADMIN = 'ADMIN', _('Админ')
