# Generated by Django 4.1.6 on 2023-02-13 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_group_status_alter_group_hotel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='tag',
            field=models.CharField(max_length=25, unique=True, verbose_name='Тег группы'),
        ),
    ]
