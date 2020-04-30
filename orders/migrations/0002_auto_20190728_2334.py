# Generated by Django 2.2.3 on 2019-07-28 17:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(max_length=12, validators=[django.core.validators.RegexValidator(code='invalid_phone_number', message='Please enter a valid phone number. For example, 87001112233 or +77001112233', regex='^(8|(+7))\\d{10}$')]),
        ),
    ]