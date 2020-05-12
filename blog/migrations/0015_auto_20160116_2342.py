# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_numberquery_free'),
    ]

    operations = [
        migrations.RenameField(
            model_name='numberquery',
            old_name='free',
            new_name='number',
        ),
        migrations.AlterField(
            model_name='numberfact',
            name='unit',
            field=models.CharField(choices=[('km', 'kilometer'), ('m', 'meter'), ('cm', 'centimeter'), ('mm', 'millimeter'), ('mile', 'mile'), ('yard', 'yard'), ('foot', 'foot'), ('inch', 'inch'), ('i', 'item'), ('USD', 'US Dollars (USD)'), ('AUD', 'Australian Dollar (AUD)'), ('CAD', 'Canadian Dollar (CAD)'), ('CHF', 'Swiss Franc (CHF)'), ('EUR', 'Euros (EUR)'), ('GBP', 'UK Pounds (GBP)'), ('HKD', 'Hongkong Dollar (HKD)'), ('JPY', 'Japanese Yen (JPY)'), ('year', 'year'), ('month', 'month'), ('week', 'week'), ('day', 'day'), ('hour', 'hour'), ('minute', 'minute'), ('second', 'second')], max_length=10),
        ),
        migrations.AlterField(
            model_name='numberquery',
            name='target_unit',
            field=models.CharField(choices=[('km', 'kilometer'), ('m', 'meter'), ('cm', 'centimeter'), ('mm', 'millimeter'), ('mile', 'mile'), ('yard', 'yard'), ('foot', 'foot'), ('inch', 'inch'), ('i', 'item'), ('USD', 'US Dollars (USD)'), ('AUD', 'Australian Dollar (AUD)'), ('CAD', 'Canadian Dollar (CAD)'), ('CHF', 'Swiss Franc (CHF)'), ('EUR', 'Euros (EUR)'), ('GBP', 'UK Pounds (GBP)'), ('HKD', 'Hongkong Dollar (HKD)'), ('JPY', 'Japanese Yen (JPY)'), ('year', 'year'), ('month', 'month'), ('week', 'week'), ('day', 'day'), ('hour', 'hour'), ('minute', 'minute'), ('second', 'second')], max_length=10),
        ),
        migrations.AlterField(
            model_name='numberquery',
            name='unit',
            field=models.CharField(choices=[('km', 'kilometer'), ('m', 'meter'), ('cm', 'centimeter'), ('mm', 'millimeter'), ('mile', 'mile'), ('yard', 'yard'), ('foot', 'foot'), ('inch', 'inch'), ('i', 'item'), ('USD', 'US Dollars (USD)'), ('AUD', 'Australian Dollar (AUD)'), ('CAD', 'Canadian Dollar (CAD)'), ('CHF', 'Swiss Franc (CHF)'), ('EUR', 'Euros (EUR)'), ('GBP', 'UK Pounds (GBP)'), ('HKD', 'Hongkong Dollar (HKD)'), ('JPY', 'Japanese Yen (JPY)'), ('year', 'year'), ('month', 'month'), ('week', 'week'), ('day', 'day'), ('hour', 'hour'), ('minute', 'minute'), ('second', 'second')], max_length=10),
        ),
    ]
