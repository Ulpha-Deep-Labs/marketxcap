# Generated by Django 5.0.3 on 2024-03-16 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_rename_last_updated_commodity_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commodity',
            name='average_price',
        ),
        migrations.RemoveField(
            model_name='commodity',
            name='highest_price',
        ),
        migrations.RemoveField(
            model_name='commodity',
            name='lowest_price',
        ),
    ]