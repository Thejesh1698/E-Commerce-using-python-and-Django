# Generated by Django 3.0.5 on 2020-04-22 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0001_initial'),
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='billing_address',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='billing.BillingAddress'),
        ),
    ]
