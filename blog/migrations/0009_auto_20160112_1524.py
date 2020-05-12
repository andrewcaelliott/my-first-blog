# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_numberquery_target_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='numberfact',
            name='multiple',
            field=models.CharField(max_length=1, choices=[('U', 'single'), ('K', 'thousand'), ('M', 'million'), ('G', 'billion'), ('T', 'trillion')]),
        ),
        migrations.AlterField(
            model_name='numberquery',
            name='multiple',
            field=models.CharField(max_length=1, default='U', choices=[('U', 'single'), ('K', 'thousand'), ('M', 'million'), ('G', 'billion'), ('T', 'trillion')]),
        ),
    ]
