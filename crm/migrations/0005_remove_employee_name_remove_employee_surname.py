# Generated by Django 4.1.6 on 2023-02-13 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_alter_group_tag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='name',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='surname',
        ),
    ]
