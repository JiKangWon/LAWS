# Generated by Django 5.1.1 on 2024-12-31 14:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0019_alter_daypathway_classobj'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='balance',
        ),
        migrations.AddField(
            model_name='transaction',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_site.user', verbose_name='User'),
        ),
        migrations.AddField(
            model_name='user',
            name='balance',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Balance'),
        ),
        migrations.AlterField(
            model_name='sessionpathway',
            name='ordinal',
            field=models.IntegerField(default=0, verbose_name='Số thứ tự của buổi học'),
        ),
        migrations.AlterField(
            model_name='sessionpathway',
            name='status',
            field=models.BooleanField(default=False, verbose_name='Trạng thái buổi học'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.CharField(default='unexpected_expenses', max_length=50, verbose_name='Loại giao dịch'),
        ),
        migrations.DeleteModel(
            name='Balance',
        ),
    ]
