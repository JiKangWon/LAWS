# Generated by Django 5.1.1 on 2024-12-30 10:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0018_class_maxofday_class_maxofsessionsinday_daypathway_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daypathway',
            name='classObj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_site.class', verbose_name='Thông tin lớp học'),
        ),
    ]