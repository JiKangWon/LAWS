# Generated by Django 5.1.1 on 2024-12-16 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0004_remove_chapter_link_course_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='end',
        ),
    ]
