# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-17 05:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wikiblog', '0007_auto_20160317_0509'),
    ]

    operations = [
        migrations.AddField(
            model_name='hashtag',
            name='page',
            field=models.ManyToManyField(to='wikiblog.Page'),
        ),
    ]