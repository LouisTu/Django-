# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-19 06:57
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20171119_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepost',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 19, 6, 57, 41, 548602, tzinfo=utc)),
        ),
    ]
