# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20160115_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='numberquery',
            name='free',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
