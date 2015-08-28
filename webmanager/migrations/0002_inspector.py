# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webmanager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inspector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status_code', models.IntegerField(max_length=3)),
                ('method', models.CharField(max_length=5)),
                ('host', models.CharField(max_length=50)),
                ('url', models.CharField(max_length=50)),
                ('request', models.TextField()),
                ('response', models.TextField()),
            ],
        ),
    ]
