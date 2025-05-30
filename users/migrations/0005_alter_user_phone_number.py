# Generated by Django 5.2.1 on 2025-05-21 13:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=12, unique=True, validators=[django.core.validators.RegexValidator(message='Номер телефона должен быть введен в формате: "+79999999999". Допускается до 12 цифр.', regex='^\\+?1?\\d{9,12}$')], verbose_name='Номер телефона'),
        ),
    ]
