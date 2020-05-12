# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_numberfact_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='NumberQuery',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('title', models.CharField(max_length=50)),
                ('number', models.CharField(max_length=20)),
                ('scale', models.IntegerField()),
                ('location', models.CharField(max_length=100)),
                ('value', models.DecimalField(max_digits=30, decimal_places=10)),
                ('unit', models.CharField(max_length=10)),
                ('subject', models.TextField()),
            ],
        ),
    ]
