# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20160112_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='numberquery',
            name='unit',
            field=models.CharField(max_length=10, choices=[('i', 'item')]),
        ),
    ]
