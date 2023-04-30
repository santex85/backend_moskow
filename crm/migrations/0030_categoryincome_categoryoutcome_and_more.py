# Generated by Django 4.1.6 on 2023-04-26 03:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0029_alter_cashier_services'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryIncome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название категории')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание категории')),
            ],
            options={
                'verbose_name': 'Категория прихода',
                'verbose_name_plural': 'Категории прихода',
            },
        ),
        migrations.CreateModel(
            name='CategoryOutcome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название категории')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание категории')),
            ],
            options={
                'verbose_name': 'Категория расхода',
                'verbose_name_plural': 'Категории расхода',
            },
        ),
        migrations.RemoveField(
            model_name='cashier',
            name='services',
        ),
        migrations.AddField(
            model_name='cashier',
            name='comment',
            field=models.TextField(default=1, verbose_name='Комментарий'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Service',
        ),
        migrations.AddField(
            model_name='cashier',
            name='category_income',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.categoryincome', verbose_name='Категория прихода'),
        ),
        migrations.AddField(
            model_name='cashier',
            name='category_outcome',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.categoryoutcome', verbose_name='Категория расхода'),
        ),
    ]
