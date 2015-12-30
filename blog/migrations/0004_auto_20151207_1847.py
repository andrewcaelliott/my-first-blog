# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_numberfact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='numberFact',
            field=models.ForeignKey(default=-1, to='blog.NumberFact'),
        ),
    ]
