import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _

# Create your models here.
from apps.core.models import TimestampModel
from apps.users import RoleTypes
from apps.users.managers import UserManager


class NameModel(models.Model):
    first_name = models.CharField(_("Имя"), max_length=150, null=True)
    last_name = models.CharField(_("Фамилия"), max_length=150, null=True)
    middle_name = models.CharField(_("Отчество"), max_length=150, null=True, blank=True)
    mobile_phone  = PhoneNumberField("Мобильный телефон", null=True)
    class Meta:
        abstract = True

    @property
    def full_name(self) -> str:
        return " ".join(
            filter(None, [self.last_name, self.first_name, self.middle_name])
        )


class User(NameModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)

    role = models.CharField('Роль', choices=RoleTypes.choices, max_length=100, default=RoleTypes.BUYER)

    is_active = models.BooleanField("Активный", default=True)
    is_staff = models.BooleanField("Сотрудник", default=False)

    secret_key = models.UUIDField("Секретный ключ", default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField("Создан", default=timezone.localtime)
    updated_at = models.DateTimeField("Обновлен", auto_now=True)

    objects = UserManager()

    class Meta:
        verbose_name="Пользователь"
        verbose_name_plural="Пользователи"

    def __str__(self):
        return self.email

    USERNAME_FIELD = 'email'

    def get_username(self):
        return self.email