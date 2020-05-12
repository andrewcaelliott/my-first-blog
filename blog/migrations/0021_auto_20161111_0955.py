# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0020_auto_20160509_0843'),
    ]

    operations = [
        migrations.AddField(
            model_name='numberfact',
            name='date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='numberfact',
            name='measure',
            field=models.CharField(choices=[('c', 'count'), ('a', 'amount'), ('e', 'extent'), ('d', 'duration'), ('n', 'number'), ('m', 'mass'), ('r', 'area'), ('v', 'volume')], max_length=1),
        ),
        migrations.AlterField(
            model_name='numberfact',
            name='permlink',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='numberquery',
            name='measure',
            field=models.CharField(choices=[('c', 'count'), ('a', 'amount'), ('e', 'extent'), ('d', 'duration'), ('n', 'number'), ('m', 'mass'), ('r', 'area'), ('v', 'volume')], default='c', max_length=1),
        ),
    ]
