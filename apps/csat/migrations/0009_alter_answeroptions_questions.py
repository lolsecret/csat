# Generated by Django 3.2.5 on 2021-07-17 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csat', '0008_auto_20210717_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answeroptions',
            name='questions',
            field=models.ManyToManyField(related_name='answer_options', to='csat.ApplicationQuestion', verbose_name='Вопросы'),
        ),
    ]
