# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_numberfact'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='numberFact',
            field=models.ForeignKey(default=None, to='blog.NumberFact'),
            preserve_default=False,
        ),
    ]
