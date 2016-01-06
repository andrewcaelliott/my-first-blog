# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_numberfact_scale'),
    ]

    operations = [
        migrations.AddField(
            model_name='numberfact',
            name='location',
            field=models.CharField(default='/', max_length=100),
            preserve_default=False,
        ),
    ]
