# Generated by Django 5.1.1 on 2025-01-01 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0027_alter_typeoftransaction_maxvalue'),
    ]

    operations = [
        migrations.AddField(
            model_name='typeoftransaction',
            name='month',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='typeoftransaction',
            name='year',
            field=models.IntegerField(default=2025, verbose_name='Năm'),
        ),
    ]
