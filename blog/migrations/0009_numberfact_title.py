# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_numberfact_referent'),
    ]

    operations = [
        migrations.AddField(
            model_name='numberfact',
            name='title',
            field=models.CharField(default='default', max_length=50),
            preserve_default=False,
        ),
    ]
