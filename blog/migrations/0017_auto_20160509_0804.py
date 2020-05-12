# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_auto_20160120_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='numberquery',
            name='slug',
            field=models.SlugField(default='slug', unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='numberfact',
            name='measure',
            field=models.CharField(choices=[('c', 'count'), ('a', 'amount'), ('e', 'extent'), ('d', 'duration'), ('n', 'number'), ('m', 'mass')], max_length=1),
        ),
        migrations.AlterField(
            model_name='numberfact',
            name='multiple',
            field=models.CharField(choices=[('U', '-'), ('k', 'thousand'), ('M', 'million'), ('G', 'billion'), ('T', 'trillion'), ('P', 'quadrillion'), ('E', 'quintillion'), ('Z', 'sextillion'), ('Y', 'septillion'), ('10^27', '10^27'), ('10^30', '10^30'), ('10^33', '10^33'), ('10^36', '10^36'), ('10^39', '10^39'), ('10^42', '10^42')], max_length=1),
        ),
        migrations.AlterField(
            model_name='numberfact',
            name='unit',
            field=models.CharField(choices=[('km', 'kilometer'), ('m', 'meter'), ('cm', 'centimeter'), ('mm', 'millimeter'), ('mile', 'mile'), ('yard', 'yard'), ('foot', 'foot'), ('inch', 'inch'), ('i', 'item'), ('USD', 'US Dollars (USD)'), ('AUD', 'Australian Dollar (AUD)'), ('CAD', 'Canadian Dollar (CAD)'), ('CHF', 'Swiss Franc (CHF)'), ('EUR', 'Euros (EUR)'), ('GBP', 'UK Pounds (GBP)'), ('HKD', 'Hongkong Dollar (HKD)'), ('JPY', 'Japanese Yen (JPY)'), ('year', 'year'), ('month', 'month'), ('week', 'week'), ('day', 'day'), ('hour', 'hour'), ('minute', 'minute'), ('second', 'second'), ('t', 'metric_ton'), ('kg', 'kilogram'), ('g', 'gram'), ('ton', 'ton'), ('st', 'stone'), ('lb', 'pound')], max_length=10),
        ),
        migrations.AlterField(
            model_name='numberquery',
            name='measure',
            field=models.CharField(default='c', choices=[('c', 'count'), ('a', 'amount'), ('e', 'extent'), ('d', 'duration'), ('n', 'number'), ('m', 'mass')], max_length=1),
        ),
        migrations.AlterField(
            model_name='numberquery',
            name='multiple',
            field=models.CharField(default='U', choices=[('U', '-'), ('k', 'thousand'), ('M', 'million'), ('G', 'billion'), ('T', 'trillion'), ('P', 'quadrillion'), ('E', 'quintillion'), ('Z', 'sextillion'), ('Y', 'septillion'), ('10^27', '10^27'), ('10^30', '10^30'), ('10^33', '10^33'), ('10^36', '10^36'), ('10^39', '10^39'), ('10^42', '10^42')], max_length=1),
        ),
        migrations.AlterField(
            model_name='numberquery',
            name='number',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='numberquery',
            name='target_unit',
            field=models.CharField(choices=[('km', 'kilometer'), ('m', 'meter'), ('cm', 'centimeter'), ('mm', 'millimeter'), ('mile', 'mile'), ('yard', 'yard'), ('foot', 'foot'), ('inch', 'inch'), ('i', 'item'), ('USD', 'US Dollars (USD)'), ('AUD', 'Australian Dollar (AUD)'), ('CAD', 'Canadian Dollar (CAD)'), ('CHF', 'Swiss Franc (CHF)'), ('EUR', 'Euros (EUR)'), ('GBP', 'UK Pounds (GBP)'), ('HKD', 'Hongkong Dollar (HKD)'), ('JPY', 'Japanese Yen (JPY)'), ('year', 'year'), ('month', 'month'), ('week', 'week'), ('day', 'day'), ('hour', 'hour'), ('minute', 'minute'), ('second', 'second'), ('t', 'metric_ton'), ('kg', 'kilogram'), ('g', 'gram'), ('ton', 'ton'), ('st', 'stone'), ('lb', 'pound')], max_length=10),
        ),
        migrations.AlterField(
            model_name='numberquery',
            name='unit',
            field=models.CharField(choices=[('km', 'kilometer'), ('m', 'meter'), ('cm', 'centimeter'), ('mm', 'millimeter'), ('mile', 'mile'), ('yard', 'yard'), ('foot', 'foot'), ('inch', 'inch'), ('i', 'item'), ('USD', 'US Dollars (USD)'), ('AUD', 'Australian Dollar (AUD)'), ('CAD', 'Canadian Dollar (CAD)'), ('CHF', 'Swiss Franc (CHF)'), ('EUR', 'Euros (EUR)'), ('GBP', 'UK Pounds (GBP)'), ('HKD', 'Hongkong Dollar (HKD)'), ('JPY', 'Japanese Yen (JPY)'), ('year', 'year'), ('month', 'month'), ('week', 'week'), ('day', 'day'), ('hour', 'hour'), ('minute', 'minute'), ('second', 'second'), ('t', 'metric_ton'), ('kg', 'kilogram'), ('g', 'gram'), ('ton', 'ton'), ('st', 'stone'), ('lb', 'pound')], max_length=10),
        ),
    ]
