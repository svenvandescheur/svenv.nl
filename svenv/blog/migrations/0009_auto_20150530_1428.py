# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20150530_1331'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='url_title',
            new_name='short_title',
        ),
    ]
