# Generated by Django 3.2.5 on 2021-07-16 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('csat', '0004_alter_applicationform_is_expired'),
    ]

    operations = [
        migrations.RenameField(
            model_name='applicationquestion',
            old_name='questions',
            new_name='application',
        ),
    ]