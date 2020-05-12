# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20160108_0925'),
    ]

    operations = [
        migrations.AddField(
            model_name='numberfact',
            name='measure',
            field=models.CharField(default='count', choices=[('c', 'count'), ('a', 'amount'), ('e', 'extent'), ('d', 'duration'), ('n', 'number')], max_length=1),
            preserve_default=False,
        ),
    ]
