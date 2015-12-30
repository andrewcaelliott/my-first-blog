# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20151207_1944'),
    ]

    operations = [
        migrations.AddField(
            model_name='numberfact',
            name='referent',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
