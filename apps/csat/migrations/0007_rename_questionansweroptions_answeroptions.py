# Generated by Django 3.2.5 on 2021-07-17 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('csat', '0006_questionansweroptions'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='QuestionAnswerOptions',
            new_name='AnswerOptions',
        ),
    ]
