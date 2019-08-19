# Generated by Django 2.2.3 on 2019-07-28 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20190728_2345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Наличные курьеру'), (2, 'Банковская карта')], default=1),
        ),
        migrations.AlterField(
            model_name='orderstatus',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Упаковано'), (2, 'Отправлено'), (3, 'Доставлено'), (4, 'Заменено'), (5, 'Возвращено'), (6, 'Отменено')], default=1),
        ),
    ]
