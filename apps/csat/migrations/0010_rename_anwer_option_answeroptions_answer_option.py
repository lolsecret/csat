# Generated by Django 3.2.5 on 2021-07-17 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('csat', '0009_alter_answeroptions_questions'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answeroptions',
            old_name='anwer_option',
            new_name='answer_option',
        ),
    ]
