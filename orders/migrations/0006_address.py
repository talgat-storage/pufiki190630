# Generated by Django 2.2.3 on 2019-08-17 09:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20190729_0007'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.PositiveSmallIntegerField(choices=[(1, 'Almaty'), (2, 'Nur-Sultan'), (3, 'Aktau'), (4, 'Aktobe'), (5, 'Atyrau'), (6, 'Aksay'), (7, 'Akkol'), (8, 'Balhash'), (9, 'Zhezkazgan'), (10, 'Karaganda'), (11, 'Kokshetau'), (12, 'Kostanay'), (13, 'Kyzylorda'), (14, 'Taldykorgan'), (15, 'Taraz'), (16, 'Temirtau'), (17, 'Uralsk'), (18, 'Ust-Kamenogorsk'), (19, 'Pavlodar'), (20, 'Petropavlovsk'), (21, 'Semey'), (22, 'Shymkent'), (23, 'Shuchinsk'), (24, 'Ekibastuz')], default=1)),
                ('house', models.CharField(max_length=16, null=True)),
                ('flat', models.CharField(max_length=16, null=True)),
                ('phone', models.CharField(max_length=12, validators=[django.core.validators.RegexValidator(code='invalid_phone_number', message='Пожалуйста, введите номер телефона в формате 87001112233 или +77001112233', regex='^(8|(\\+7))\\d{10}$')])),
            ],
        ),
    ]
