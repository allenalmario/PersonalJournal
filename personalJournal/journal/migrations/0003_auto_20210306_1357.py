# Generated by Django 2.2.4 on 2021-03-06 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0002_auto_20210306_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='desc',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='entry',
            name='title',
            field=models.CharField(max_length=80),
        ),
    ]
