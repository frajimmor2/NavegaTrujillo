# Generated by Django 5.1.3 on 2024-11-26 15:02

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0005_alter_reservation_port_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='rental_end_date',
            field=models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(2024, 11, 26))]),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='rental_start_date',
            field=models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(2024, 11, 26))]),
        ),
        migrations.AlterField(
            model_name='shopping_basket',
            name='rental_end_date',
            field=models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(2024, 11, 26))]),
        ),
        migrations.AlterField(
            model_name='shopping_basket',
            name='rental_start_date',
            field=models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(2024, 11, 26))]),
        ),
    ]
