# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_numberquery_measure'),
    ]

    operations = [
        migrations.AddField(
            model_name='numberquery',
            name='target_unit',
            field=models.CharField(max_length=10, default=''),
            preserve_default=False,
        ),
    ]
