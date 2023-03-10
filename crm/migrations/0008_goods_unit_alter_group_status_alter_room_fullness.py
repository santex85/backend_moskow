# Generated by Django 4.1.6 on 2023-02-16 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0007_room_number_guests_alter_room_fullness'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='unit',
            field=models.CharField(choices=[('volume', 'л.'), ('weight', 'кг.'), ('quantity', 'шт.')], default=1, max_length=256, verbose_name='Единица измерения'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='group',
            name='status',
            field=models.CharField(choices=[('preregister', 'Предварительная регистрация'), ('register', 'Регистрация'), ('inhotel', 'В отеле'), ('finish', 'Завершен')], default='Предварительная регистрация', max_length=30, verbose_name='Статус группы'),
        ),
        migrations.AlterField(
            model_name='room',
            name='fullness',
            field=models.CharField(choices=[('full', 'Полный'), ('partially', 'Частично'), ('empty', 'Пустой'), ('over', 'Переполненный')], default='empty', max_length=30, verbose_name='Статус'),
        ),
    ]
