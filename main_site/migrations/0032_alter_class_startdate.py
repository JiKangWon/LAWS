# Generated by Django 5.1.1 on 2025-01-11 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0031_deadline_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='startDate',
            field=models.DateField(null=True, verbose_name='Thời gian mở lớp'),
        ),
    ]
