# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TarnhelmAuth', '0002_logintoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logintoken',
            name='is_anonymous',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
