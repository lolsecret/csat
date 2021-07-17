import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
from apps.core.models import TimestampModel


class Person(models.Model):
    iin = models.CharField("ИИН", max_length=12)
    mobile_phone = PhoneNumberField("Мобильный телефон")
    class Meta:
        verbose_name = "Физ. лицо"
        verbose_name_plural = "Физ. лица"

    def __str__(self):
        return self.iin

    @property
    def user_exists(self):
        return hasattr(self, "user")


class User(PermissionsMixin, AbstractBaseUser, TimestampModel):
    email = models.EmailField("Email", unique=True, null=True)
    person = models.OneToOneField(
        Person,
        related_name="user",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Физ. лицо",
    )
    username = models.CharField(max_length=100, unique=True, null=True)
    is_active = models.BooleanField("Активный", default=True)
    is_staff = models.BooleanField("Сотрудник", default=False)
    USERNAME_FIELD = "email"
    secret_key = models.UUIDField("Секретный ключ", default=uuid.uuid4, unique=True)

    objects = UserManager()

    REQUIRED_FIELDS = ['username']
    def has_perm(self, perm, obj=None):
        if not self.is_active:
            return False

        if self.is_superuser:
            return True

        return perm in self.get_all_permissions(obj)

    def has_module_perms(self, app_label):
        if self.is_superuser:
            return True
        return self.is_active and any(
            perm[: perm.index(".")] == app_label for perm in self.get_all_permissions()
        )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        if self.person:
            return self.person.iin
        if self.email:
            return self.email
        return str(self.pk)