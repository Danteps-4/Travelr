# Generated by Django 5.1.7 on 2025-03-18 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('explore', '0002_rename_date_visit_date_visit_visit_profile_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Visit',
        ),
    ]
