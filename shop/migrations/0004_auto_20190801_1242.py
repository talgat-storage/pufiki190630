# Generated by Django 2.2.3 on 2019-08-01 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20190801_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='origin',
            name='description',
            field=models.TextField(default=''),
        ),
    ]
