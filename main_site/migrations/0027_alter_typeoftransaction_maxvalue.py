# Generated by Django 5.1.1 on 2024-12-31 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0026_typeoftransaction_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typeoftransaction',
            name='maxValue',
            field=models.IntegerField(verbose_name='Hạn mức tối đa mỗi tháng'),
        ),
    ]