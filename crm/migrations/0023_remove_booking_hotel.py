# Generated by Django 4.1.6 on 2023-03-20 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0022_guest_room'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='hotel',
        ),
    ]