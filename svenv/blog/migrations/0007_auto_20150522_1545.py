# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_page_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 22, 15, 45, 39, 328889, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 22, 15, 45, 43, 201103, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='image',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 22, 15, 45, 45, 217137, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='image',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 22, 15, 45, 47, 289197, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='page',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 22, 15, 45, 49, 497910, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 22, 15, 45, 51, 977471, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
