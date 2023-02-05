# Generated by Django 4.1.6 on 2023-02-04 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Ингридиент')),
                ('count', models.IntegerField(verbose_name='Объем/количество')),
                ('cost', models.IntegerField(verbose_name='Стоимость')),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Имя отеля')),
            ],
        ),
        migrations.CreateModel(
            name='Groceries',
            fields=[
                ('goods_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='crm.goods')),
            ],
            bases=('crm.goods',),
        ),
        migrations.CreateModel(
            name='Household',
            fields=[
                ('goods_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='crm.goods')),
            ],
            bases=('crm.goods',),
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Номер комнаты')),
                ('name', models.CharField(blank=True, max_length=256, null=True, verbose_name='Название комнаты')),
                ('capacity', models.IntegerField(default=2, verbose_name='Количество мест')),
                ('over_booking', models.IntegerField(verbose_name='Дополнительные места в номер')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.hotel')),
            ],
        ),
    ]
