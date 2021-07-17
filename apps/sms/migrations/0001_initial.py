# Generated by Django 3.2.5 on 2021-07-16 17:09

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SMSMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Время создания')),
                ('changed_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Время последнего изменения')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Идентификатор')),
                ('recipients', models.CharField(editable=False, max_length=255, verbose_name='Получатель')),
                ('content', models.TextField(editable=False, verbose_name='Содержимое')),
                ('sending_time', models.DateTimeField(null=True, verbose_name='Время отправки смс')),
                ('additional_data', django.contrib.postgres.fields.jsonb.JSONField(editable=False, null=True, verbose_name='Доп. информация')),
                ('error_code', models.IntegerField(editable=False, null=True, verbose_name='Код ошибки')),
                ('error_description', models.CharField(editable=False, max_length=255, null=True, verbose_name='Описание ошибки')),
            ],
            options={
                'verbose_name': 'SMS сообщение',
                'verbose_name_plural': 'SMS сообщения',
            },
        ),
    ]
