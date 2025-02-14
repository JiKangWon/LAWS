# Generated by Django 5.1.1 on 2024-12-25 11:58

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0013_alter_session_chapter'),
    ]

    operations = [
        migrations.RenameField(
            model_name='balance',
            old_name='balance',
            new_name='value',
        ),
        migrations.RenameField(
            model_name='class',
            old_name='end_time',
            new_name='endDate',
        ),
        migrations.RenameField(
            model_name='class',
            old_name='start_time',
            new_name='startDate',
        ),
        migrations.RenameField(
            model_name='term',
            old_name='start_date',
            new_name='startDate',
        ),
        migrations.RenameField(
            model_name='term',
            old_name='total_of_months',
            new_name='totalOfMonths',
        ),
        migrations.RenameField(
            model_name='userinfo',
            old_name='phone_number',
            new_name='phoneNumber',
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='course',
        ),
        migrations.RemoveField(
            model_name='contentofchapters',
            name='number',
        ),
        migrations.RemoveField(
            model_name='session',
            name='class_obj',
        ),
        migrations.RemoveField(
            model_name='session',
            name='course',
        ),
        migrations.RemoveField(
            model_name='session',
            name='date',
        ),
        migrations.RemoveField(
            model_name='shift',
            name='date',
        ),
        migrations.RemoveField(
            model_name='term',
            name='end_date',
        ),
        migrations.AddField(
            model_name='chapter',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_site.subject', verbose_name='Subject of this chapter'),
        ),
        migrations.AddField(
            model_name='session',
            name='classObj',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_site.class', verbose_name='Class in this session'),
        ),
        migrations.AddField(
            model_name='session',
            name='endTime',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='End Time'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='session',
            name='startTime',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Start Time'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shift',
            name='endTime',
            field=models.DateTimeField(auto_now=True, verbose_name='End time of Shift'),
        ),
        migrations.AddField(
            model_name='shift',
            name='startTime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Start time of Shift'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shift',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_site.user', verbose_name='User of this Shift'),
        ),
        migrations.AddField(
            model_name='term',
            name='endDate',
            field=models.DateField(blank=True, null=True, verbose_name='Ngày kết thúc'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='type',
            field=models.CharField(choices=[('monthly_income', 'monthly income'), ('salary', 'salary'), ('other_earnings', 'other earnings'), ('food expenses', 'food expenses'), ('transportation_expenses', 'Transportation expenses'), ('entertainment_expenses', 'entertainment expenses'), ('unexpected_expenses', 'unexpected expenses'), ('monthly_rent', 'monthly rent'), ('study_materials_expenses', 'Study materials Expenses')], default='unexpected_expenses', max_length=50, verbose_name='Loại giao dịch'),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='number',
            field=models.IntegerField(verbose_name='Ordinal Number'),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='title',
            field=models.CharField(max_length=250, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='contentofchapters',
            name='chapter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_site.chapter', verbose_name='Chapter of this Content'),
        ),
        migrations.AlterField(
            model_name='contentofchapters',
            name='content',
            field=models.TextField(verbose_name='Content'),
        ),
        migrations.AlterField(
            model_name='contentofchapters',
            name='link',
            field=models.URLField(max_length=250, verbose_name='Link to Tutorial'),
        ),
        migrations.AlterField(
            model_name='contentofchapters',
            name='title',
            field=models.TextField(max_length=250, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='session',
            name='chapter',
            field=models.ManyToManyField(blank=True, to='main_site.chapter', verbose_name='Chapter in this session'),
        ),
        migrations.AlterField(
            model_name='session',
            name='note',
            field=models.TextField(verbose_name='Note'),
        ),
        migrations.AlterField(
            model_name='session',
            name='shift',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_site.shift', verbose_name='Shift for this Session'),
        ),
        migrations.AlterField(
            model_name='session',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_site.subject', verbose_name='Subject in this session'),
        ),
        migrations.AlterField(
            model_name='session',
            name='type',
            field=models.CharField(choices=[('learn', 'learn'), ('review', 'review'), ('practice', 'practice')], default='learn', max_length=10),
        ),
        migrations.AlterField(
            model_name='shift',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Name of Shift '),
        ),
    ]
