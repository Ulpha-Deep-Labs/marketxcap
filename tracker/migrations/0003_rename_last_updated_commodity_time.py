# Generated by Django 5.0.3 on 2024-03-16 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_commodity_delete_pricetracking'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commodity',
            old_name='last_updated',
            new_name='time',
        ),
    ]
