# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-29 02:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wikiblog', '0019_auto_20160329_0253'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_page_accessed',
            name='user_page_from',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='wikiblog.User_page_accessed'),
        ),
    ]
