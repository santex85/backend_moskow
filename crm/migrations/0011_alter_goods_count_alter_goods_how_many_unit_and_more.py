# Generated by Django 4.1.6 on 2023-02-17 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0010_goods_how_many_unit_alter_goods_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='count',
            field=models.FloatField(verbose_name='Объем/количество в единице'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='how_many_unit',
            field=models.FloatField(default=0, verbose_name='Количество единиц'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='name',
            field=models.CharField(max_length=250, unique=True, verbose_name='Название товара'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='unit',
            field=models.CharField(choices=[('volume', 'л.'), ('weight', 'кг.'), ('quantity', 'шт.')], default='weight', max_length=256, verbose_name='Единица измерения'),
        ),
    ]
