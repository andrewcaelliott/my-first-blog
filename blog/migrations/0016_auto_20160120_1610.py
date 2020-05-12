# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_auto_20160116_2342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='numberfact',
            name='value',
            field=models.FloatField(),
        ),
    ]
