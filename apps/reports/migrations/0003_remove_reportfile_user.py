# Generated by Django 3.2.5 on 2021-07-17 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_alter_reportfile_filter_types'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reportfile',
            name='user',
        ),
    ]
