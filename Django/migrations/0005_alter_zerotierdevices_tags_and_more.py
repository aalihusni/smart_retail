# Generated by Django 4.2.13 on 2024-05-26 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Django', '0004_alter_zerotierdevices_last_online_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zerotierdevices',
            name='tags',
            field=models.JSONField(default='{}', verbose_name=dict),
        ),
        migrations.AlterField(
            model_name='zerotierrequestaccess',
            name='tags',
            field=models.JSONField(default='{}', verbose_name=dict),
        ),
    ]
