# Generated by Django 5.1.3 on 2024-11-21 10:47

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0003_remove_shopping_basket_client_client_shopping_basket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='rental_end_date',
            field=models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(2024, 11, 21))]),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='rental_start_date',
            field=models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(2024, 11, 21))]),
        ),
        migrations.AlterField(
            model_name='shopping_basket',
            name='rental_end_date',
            field=models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(2024, 11, 21))]),
        ),
        migrations.AlterField(
            model_name='shopping_basket',
            name='rental_start_date',
            field=models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(2024, 11, 21))]),
        ),
    ]
