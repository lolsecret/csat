# Generated by Django 3.2.5 on 2021-07-16 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('csat', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicationform',
            name='questions',
        ),
        migrations.AddField(
            model_name='applicationquestion',
            name='questions',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='csat.applicationform', verbose_name='Опросник'),
        ),
    ]
