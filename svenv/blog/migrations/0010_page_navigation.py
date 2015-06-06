# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20150530_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='navigation',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
    ]
