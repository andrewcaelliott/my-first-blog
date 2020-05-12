# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_numberquery'),
    ]

    operations = [
        migrations.AddField(
            model_name='numberfact',
            name='multiple',
            field=models.CharField(choices=[('K', 'thousand'), ('M', 'million'), ('G', 'billion'), ('T', 'trillion')], max_length=1, default='U'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='numberquery',
            name='multiple',
            field=models.CharField(choices=[('U', 'unit'), ('K', 'thousand'), ('M', 'million'), ('G', 'billion'), ('T', 'trillion')], max_length=1, default='U'),
        ),
    ]
