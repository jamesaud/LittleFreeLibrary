# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-18 03:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wikiblog', '0009_auto_20160317_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
