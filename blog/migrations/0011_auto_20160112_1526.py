# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20160112_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='numberfact',
            name='unit',
            field=models.CharField(choices=[('i', 'item')], max_length=10),
        ),
    ]
