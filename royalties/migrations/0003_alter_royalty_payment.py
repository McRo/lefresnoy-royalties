# Generated by Django 5.0.6 on 2024-06-11 13:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('royalties', '0002_alter_payment_purchase_order_alter_royalty_payment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='royalty',
            name='payment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='royalty', to='royalties.payment'),
        ),
    ]
