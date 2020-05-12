# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_numberfact_measure'),
    ]

    operations = [
        migrations.AddField(
            model_name='numberquery',
            name='measure',
            field=models.CharField(default='c', choices=[('c', 'count'), ('a', 'amount'), ('e', 'extent'), ('d', 'duration'), ('n', 'number')], max_length=1),
        ),
    ]
