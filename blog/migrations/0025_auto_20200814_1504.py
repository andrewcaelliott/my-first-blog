# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0024_auto_20190614_1712'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chancefact',
            name='chance_function',
        ),
        migrations.RemoveField(
            model_name='chancequery',
            name='chance_function',
        ),
        migrations.AddField(
            model_name='chancefact',
            name='fact_type',
            field=models.CharField(max_length=10, default='fact', choices=[('fact', 'fact'), ('example', 'example'), ('proportion', 'proportion')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chancequery',
            name='form_style',
            field=models.CharField(max_length=3, default='smp'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chancequery',
            name='items',
            field=models.CharField(max_length=200, default='100 items'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chancequery',
            name='palette_name',
            field=models.CharField(max_length=10, default='default'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chancequery',
            name='repetitions',
            field=models.CharField(max_length=200, default='20 repetitions'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='chancefact',
            name='probability',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='chancequery',
            name='probability',
            field=models.CharField(max_length=150),
        ),
    ]
