# Generated by Django 5.2.1 on 2025-05-19 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal_diary', '0003_diaryentry_reminder_date_alter_diaryentry_create_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='diaryentry',
            name='reminder_time',
            field=models.TimeField(blank=True, null=True, verbose_name='Время напоминания'),
        ),
        migrations.AlterField(
            model_name='diaryentry',
            name='reminder_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата напоминания'),
        ),
    ]
