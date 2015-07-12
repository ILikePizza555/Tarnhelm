# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import TarnhelmAuth.models


class Migration(migrations.Migration):

    dependencies = [
        ('TarnhelmAuth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.CharField(default=TarnhelmAuth.models.gen_uid, max_length=40)),
                ('is_anonymous', models.BooleanField()),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
