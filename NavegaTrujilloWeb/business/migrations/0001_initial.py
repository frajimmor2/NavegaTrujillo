# Generated by Django 5.1.3 on 2024-12-01 15:37

import datetime
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_number', models.CharField(blank=True, max_length=50)),
                ('license_validated', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Port',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ubication', models.CharField(max_length=150, unique=True, validators=[django.core.validators.MinLengthValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='Ship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capacity', models.IntegerField(default=2, validators=[django.core.validators.MinValueValidator(2)])),
                ('rent_per_day', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('available', models.BooleanField(default=True)),
                ('need_license', models.BooleanField()),
                ('description', models.CharField(max_length=350, validators=[django.core.validators.MinLengthValidator(0)])),
                ('image', models.ImageField(upload_to='images/')),
                ('name', models.CharField(max_length=45, unique=True, validators=[django.core.validators.MinLengthValidator(0)])),
                ('port', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.port')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rental_start_date', models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(2024, 12, 1))])),
                ('rental_end_date', models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(2024, 12, 1))])),
                ('captain_amount', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('total_cost', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('reservation_state', models.CharField(choices=[('R', 'RESERVED'), ('P', 'RESERVED_AND_PAID'), ('C', 'CANCELED'), ('A', 'ALREADY_RENTED')], default='R', max_length=1)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='business.client')),
                ('port', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.port')),
                ('ships', models.ManyToManyField(to='business.ship')),
            ],
        ),
        migrations.CreateModel(
            name='Shopping_basket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rental_start_date', models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(2024, 12, 1))])),
                ('rental_end_date', models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(2024, 12, 1))])),
                ('captain_amount', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('ships', models.ManyToManyField(to='business.ship')),
            ],
        ),
    ]
