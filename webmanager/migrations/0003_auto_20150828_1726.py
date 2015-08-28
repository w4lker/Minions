# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webmanager', '0002_inspector'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inspector',
            name='status_code',
            field=models.IntegerField(),
        ),
    ]
