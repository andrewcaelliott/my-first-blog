# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from random import randint

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_auto_20160509_0820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='numberfact',
            name='slug',
            field=models.SlugField(default="slug", unique=False),
        ),    
        migrations.RemoveField(
            model_name='numberfact',
            name='slug',
        ),
        migrations.AddField(
            model_name='numberfact',
            name='permlink',
            field=models.SlugField(default=str(randint(0,10000000))),
            preserve_default=False,
        ),
    ]
