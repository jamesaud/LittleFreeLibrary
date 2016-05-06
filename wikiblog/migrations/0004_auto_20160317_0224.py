# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-17 02:24
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wikiblog', '0003_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['date']},
        ),
        migrations.AddField(
            model_name='page',
            name='date',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 3, 17, 2, 24, 50, 662829, tzinfo=utc)),
            preserve_default=False,
        ),
    ]