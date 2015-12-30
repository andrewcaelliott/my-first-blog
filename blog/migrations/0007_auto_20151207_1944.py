# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20151207_1855'),
    ]

    operations = [
        migrations.AddField(
            model_name='numberfact',
            name='number',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='numberfact',
            name='unit',
            field=models.CharField(default='unit', max_length=10),
            preserve_default=False,
        ),
    ]
