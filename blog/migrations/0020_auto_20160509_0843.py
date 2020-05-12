# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_auto_20160509_0823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='numberfact',
            name='permlink',
            field=models.SlugField(unique=False),
        ),
    ]
