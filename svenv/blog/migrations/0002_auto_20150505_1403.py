# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='height',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='url',
            field=models.ImageField(height_field=b'height', width_field=b'width', upload_to=b'media/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='image',
            name='width',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
