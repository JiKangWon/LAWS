# Generated by Django 5.1.1 on 2024-12-31 15:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0025_transaction_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='typeoftransaction',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_site.user'),
        ),
    ]
