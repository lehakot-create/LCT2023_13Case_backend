# Generated by Django 3.2.13 on 2022-11-01 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_auto_20221101_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='employment',
            field=models.CharField(blank=True, max_length=256, verbose_name='Занятость'),
        ),
        migrations.AddField(
            model_name='profile',
            name='experience',
            field=models.CharField(blank=True, max_length=256, verbose_name='Опыт'),
        ),
    ]
