# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20160115_1044'),
    ]

    operations = [
        migrations.RenameField(
            model_name='numberfact',
            old_name='number',
            new_name='magnitude',
        ),
        migrations.RenameField(
            model_name='numberquery',
            old_name='number',
            new_name='magnitude',
        ),
        migrations.AlterField(
            model_name='numberfact',
            name='multiple',
            field=models.CharField(choices=[('U', '-'), ('k', 'thousand'), ('M', 'million'), ('G', 'billion'), ('T', 'trillion')], max_length=1),
        ),
        migrations.AlterField(
            model_name='numberfact',
            name='unit',
            field=models.CharField(choices=[('km', 'kilometer'), ('m', 'meter'), ('cm', 'centimeter'), ('mm', 'millimeter'), ('mi', 'mile'), ('yd', 'yard'), ('ft', 'foot'), ('in', 'inch'), ('i', 'item'), ('USD', 'US Dollars (USD)'), ('AUD', 'Australian Dollar (AUD)'), ('CAD', 'Canadian Dollar (CAD)'), ('CHF', 'Swiss Franc (CHF)'), ('EUR', 'Euros (EUR)'), ('GBP', 'UK Pounds (GBP)'), ('HKD', 'Hongkong Dollar (HKD)'), ('JPY', 'Japanese Yen (JPY)'), ('year', 'year'), ('month', 'month'), ('week', 'week'), ('day', 'day'), ('hour', 'hour'), ('minute', 'minute'), ('second', 'second')], max_length=10),
        ),
        migrations.AlterField(
            model_name='numberquery',
            name='target_unit',
            field=models.CharField(choices=[('km', 'kilometer'), ('m', 'meter'), ('cm', 'centimeter'), ('mm', 'millimeter'), ('mi', 'mile'), ('yd', 'yard'), ('ft', 'foot'), ('in', 'inch'), ('i', 'item'), ('USD', 'US Dollars (USD)'), ('AUD', 'Australian Dollar (AUD)'), ('CAD', 'Canadian Dollar (CAD)'), ('CHF', 'Swiss Franc (CHF)'), ('EUR', 'Euros (EUR)'), ('GBP', 'UK Pounds (GBP)'), ('HKD', 'Hongkong Dollar (HKD)'), ('JPY', 'Japanese Yen (JPY)'), ('year', 'year'), ('month', 'month'), ('week', 'week'), ('day', 'day'), ('hour', 'hour'), ('minute', 'minute'), ('second', 'second')], max_length=10),
        ),
        migrations.AlterField(
            model_name='numberquery',
            name='unit',
            field=models.CharField(choices=[('km', 'kilometer'), ('m', 'meter'), ('cm', 'centimeter'), ('mm', 'millimeter'), ('mi', 'mile'), ('yd', 'yard'), ('ft', 'foot'), ('in', 'inch'), ('i', 'item'), ('USD', 'US Dollars (USD)'), ('AUD', 'Australian Dollar (AUD)'), ('CAD', 'Canadian Dollar (CAD)'), ('CHF', 'Swiss Franc (CHF)'), ('EUR', 'Euros (EUR)'), ('GBP', 'UK Pounds (GBP)'), ('HKD', 'Hongkong Dollar (HKD)'), ('JPY', 'Japanese Yen (JPY)'), ('year', 'year'), ('month', 'month'), ('week', 'week'), ('day', 'day'), ('hour', 'hour'), ('minute', 'minute'), ('second', 'second')], max_length=10),
        ),
    ]
