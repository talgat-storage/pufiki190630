# Generated by Django 2.2.3 on 2019-08-01 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20190801_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='color',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Красный'), (2, 'Синий'), (3, 'Зеленый'), (4, 'Фиолетовый'), (5, 'Голубой')]),
        ),
    ]
