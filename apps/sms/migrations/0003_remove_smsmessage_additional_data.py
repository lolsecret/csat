# Generated by Django 3.2.5 on 2021-07-16 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0002_alter_smsmessage_additional_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='smsmessage',
            name='additional_data',
        ),
    ]
