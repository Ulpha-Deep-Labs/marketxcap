# Generated by Django 4.2.1 on 2024-03-16 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commodity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('symbol', models.CharField(max_length=10)),
                ('current_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('highest_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('lowest_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('average_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.DeleteModel(
            name='PriceTracking',
        ),
    ]
