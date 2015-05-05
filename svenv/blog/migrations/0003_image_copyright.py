# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20150505_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='copyright',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
