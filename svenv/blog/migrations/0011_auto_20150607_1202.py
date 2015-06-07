# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_page_navigation'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='published',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='page',
            name='published',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='published',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
    ]
