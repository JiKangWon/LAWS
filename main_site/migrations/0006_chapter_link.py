# Generated by Django 5.1.1 on 2024-12-22 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0005_remove_session_end'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='link',
            field=models.URLField(max_length=250, null=True, verbose_name='Link to Theory File'),
        ),
    ]