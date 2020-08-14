# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0025_auto_20200814_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='chancefact',
            name='page_type',
            field=models.CharField(max_length=10, default='smp', choices=[('sng', 'sng'), ('smp', 'smp'), ('adv', 'adv'), ('scr', 'scr')]),
            preserve_default=False,
        ),
    ]
