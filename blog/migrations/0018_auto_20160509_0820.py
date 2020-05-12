# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_auto_20160509_0804'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='numberquery',
            name='slug',
        ),
        migrations.AddField(
            model_name='numberfact',
            name='slug',
            field=models.SlugField(unique=False, default='slug'),
            preserve_default=False,
        ),
    ]
