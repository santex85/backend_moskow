# Generated by Django 4.1.6 on 2023-02-22 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0017_alter_inventorycontrol_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventorycontrol',
            name='count',
            field=models.IntegerField(default=0, verbose_name='Количество'),
        ),
    ]
