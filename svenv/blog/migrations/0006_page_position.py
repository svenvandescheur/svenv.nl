# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_page_short_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='position',
            field=models.IntegerField(default=1, unique=True),
            preserve_default=False,
        ),
    ]
