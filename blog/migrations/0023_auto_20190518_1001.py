# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0022_auto_20190517_0949'),
    ]

    operations = [
        migrations.AddField(
            model_name='chancefact',
            name='repeat_mode',
            field=models.CharField(max_length=10, default='repeats', choices=[('repeats', 'repeats'), ('removes', 'removes')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chancequery',
            name='repeat_mode',
            field=models.CharField(max_length=10, default='repeats', choices=[('repeats', 'repeats'), ('removes', 'removes')]),
            preserve_default=False,
        ),
    ]
