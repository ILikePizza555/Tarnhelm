# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import TarnhelmAuth.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RegisteredUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.CharField(default=TarnhelmAuth.models.gen_uid, unique=True, max_length=40)),
                ('name', models.CharField(unique=True, max_length=250)),
                ('password_hash', models.CharField(max_length=40)),
                ('password_salt', models.CharField(max_length=6)),
                ('rank', models.PositiveIntegerField(default=0)),
                ('admin', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
