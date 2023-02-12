# Generated by Django 4.1.6 on 2023-02-12 03:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='hotel',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='crm.hotel'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='group',
            name='tag',
            field=models.CharField(max_length=25, verbose_name='Тег группы'),
        ),
    ]
