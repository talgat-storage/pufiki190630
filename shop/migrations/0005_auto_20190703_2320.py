# Generated by Django 2.2.3 on 2019-07-03 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20190703_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='color',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Красный'), (2, 'Зеленый'), (3, 'Синий'), (4, 'Желтый'), (5, 'Черный'), (6, 'Фиолетовый'), (7, 'Белый'), (8, 'Серый'), (9, 'Коричневый')]),
        ),
    ]
