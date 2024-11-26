# Generated by Django 5.1.3 on 2024-11-26 18:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('business', '0002_client_ship_quantity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='shopping_basket',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='business.shopping_basket'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='client',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='business.client'),
        ),
    ]
