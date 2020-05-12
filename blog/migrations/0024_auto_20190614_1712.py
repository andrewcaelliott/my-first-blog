# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0023_auto_20190518_1001'),
    ]

    operations = [
        migrations.AddField(
            model_name='chancefact',
            name='chance_function',
            field=models.CharField(max_length=150, default='constant(probability)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chancequery',
            name='chance_function',
            field=models.CharField(max_length=150, default='constant(probability)'),
            preserve_default=False,
        ),
    ]
